document.addEventListener("DOMContentLoaded", () => {

    const body = document.body;
    const logo = document.getElementById("floatingLogo");
    const dockSentinel = document.getElementById("dockSentinel");
    const sidebarLinks = Array.from(document.querySelectorAll(".sidebar-nav a[data-section]"));
    const sections = Array.from(document.querySelectorAll("#home, .content-section"));
    const mobileMenuButton = document.getElementById("mobileMenuButton");
    const mobileLinks = document.getElementById("mobileLinks");
    const outputStage = document.getElementById("outputStage");
    const schematicBackground = document.getElementById("schematicBackground");
    const schematicSvg = schematicBackground?.querySelector("svg");
    const masterCircuit = document.getElementById("masterCircuit");
    const sectionSignals = Array.from(document.querySelectorAll(".section-signal[data-target]"));
    const brandBanner = document.querySelector(".brand-banner");
    const developmentFlow = document.getElementById("developmentFlow");
    const flowStages = Array.from(document.querySelectorAll(".flow-stage"));
    const buildStage = document.getElementById("buildStage");
    const testStage = document.getElementById("testStage");

    const servicesStage = document.getElementById("servicesStage");
    const servicesOverview = document.getElementById("servicesOverview");
    const serviceDetails = document.getElementById("serviceDetails");
    const serviceBack = document.getElementById("serviceBack");
    const serviceCards = Array.from(document.querySelectorAll(".service-card[data-service]"));
    const serviceDetailPanels = Array.from(document.querySelectorAll(".service-detail[data-service-detail]"));
    const serviceMenuItems = Array.from(document.querySelectorAll(".service-menu-item[data-service-menu]"));

    const signalBySection = new Map(
        sectionSignals.map(signal => [signal.dataset.target, signal])
    );

    let activeSection = "home";
    let resizeTimer = null;

    function setActiveSection(id) {
        if (!id || activeSection === id) return;

        activeSection = id;

        sidebarLinks.forEach(link => {
            link.classList.toggle("active", link.dataset.section === id);
        });

        sectionSignals.forEach(signal => {
            signal.classList.toggle("is-active", signal.dataset.target === id);
        });
    }

    // Initial state before the observer fires.
    sidebarLinks.forEach(link => {
        link.classList.toggle("active", link.dataset.section === "home");
    });
    sectionSignals.forEach(signal => {
        signal.classList.toggle("is-active", signal.dataset.target === "home");
    });

    /* =====================================================
       SECTION ACTIVATION

       The middle 30% of the viewport acts as the viewing
       band. A section entering that band activates its gate.
       This replaces continuous scroll math entirely.
    ===================================================== */

    const sectionObserver = new IntersectionObserver(
        entries => {
            const visible = entries
                .filter(entry => entry.isIntersecting)
                .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

            if (visible.length) {
                setActiveSection(visible[0].target.id);
            }
        },
        {
            root: null,
            rootMargin: "-35% 0px -35% 0px",
            threshold: [0, .01, .25, .5, .75, 1]
        }
    );

    sections.forEach(section => sectionObserver.observe(section));

    /* =====================================================
       LOGO / SIDEBAR DOCK
    ===================================================== */

    if (dockSentinel) {
        const dockObserver = new IntersectionObserver(
            ([entry]) => {
                body.classList.toggle("site-docked", !entry.isIntersecting);
            },
            { threshold: 0 }
        );

        dockObserver.observe(dockSentinel);
    }

    /* =====================================================
       FOOTER COMPLETION
    ===================================================== */

    if (outputStage) {
        const footerObserver = new IntersectionObserver(
            ([entry]) => {
                body.classList.toggle(
                    "signal-complete",
                    entry.isIntersecting && entry.intersectionRatio >= .68
                );
            },
            { threshold: [0, .35, .68, 1] }
        );

        footerObserver.observe(outputStage);
    }

    /* =====================================================
       TECHNOLOGY TICKER

       Only animate it while it is actually on screen.
    ===================================================== */

    if (brandBanner) {
        const tickerObserver = new IntersectionObserver(
            ([entry]) => {
                brandBanner.classList.toggle("is-visible", entry.isIntersecting);
            },
            { threshold: .05 }
        );

        tickerObserver.observe(brandBanner);
    }

    /* =====================================================
       SCHEMATIC GEOMETRY

       Runs only after layout changes, not during scrolling.
       Each important gate is positioned inside the section
       it belongs to and the static route is rebuilt once.
    ===================================================== */

    function sectionAnchor(id) {
        const section = document.getElementById(id);
        if (!section) return 0;

        const rect = section.getBoundingClientRect();
        const top = window.scrollY + rect.top;
        const height = rect.height;

        return top + Math.min(window.innerHeight * .47, height * .38);
    }

    function sizeSchematic() {
        if (!schematicBackground || !schematicSvg || !outputStage) return 0;

        const footerTop = window.scrollY + outputStage.getBoundingClientRect().top;
        const height = Math.max(1, footerTop);
        schematicBackground.style.height = `${height}px`;
        schematicSvg.setAttribute("viewBox", `0 0 1600 ${height}`);
        return height;
    }

    function positionSectionSignals() {
        sectionSignals.forEach(signal => {
            const id = signal.dataset.target;
            const baseY = Number(signal.dataset.baseY || 0);
            const targetY = sectionAnchor(id);
            const deltaY = targetY - baseY;

            signal.setAttribute("transform", `translate(0 ${deltaY})`);
            signal.dataset.pageY = String(targetY);
        });
    }

    function buildStaticCircuit(pageHeight) {
        if (!masterCircuit || !outputStage || !pageHeight) return;

        const footerRect = outputStage.getBoundingClientRect();
        const footerCenterPixels = footerRect.left + footerRect.width / 2;
        const terminalX = (footerCenterPixels / window.innerWidth) * 1600;

        const homeY = sectionAnchor("home");
        const servicesY = sectionAnchor("services");
        const aboutY = sectionAnchor("about");
        const contactY = sectionAnchor("contact");
        const collaborateY = sectionAnchor("collaborate");

        const route = `
            M820 0
            V${homeY}
            H970
            V${servicesY}
            H1320
            V${aboutY}
            H930
            V${contactY}
            H1280
            V${collaborateY}
            H970
            V${pageHeight}
            H${terminalX}
        `;

        masterCircuit.setAttribute("d", route);
    }

    function rebuildSchematic() {
        const pageHeight = sizeSchematic();
        positionSectionSignals();
        buildStaticCircuit(pageHeight);
    }

    /* =====================================================
       SERVICE EXPLORER

       Cards slide left as one lightweight transform.
       The detail panel slides in from the right and keeps
       its service menu available on the right side.
    ===================================================== */

    let lastServiceTrigger = null;

    function syncServiceStageHeight(view = null) {
        if (!servicesStage || !servicesOverview || !serviceDetails) return;

        const activeView = view || (
            servicesStage.classList.contains("is-detail-open")
                ? serviceDetails
                : servicesOverview
        );

        const nextHeight = Math.ceil(activeView.scrollHeight);

        if (nextHeight > 0) {
            servicesStage.style.height = `${nextHeight}px`;
        }
    }

    servicesStage?.addEventListener("transitionend", event => {
        if (event.propertyName === "height") {
            rebuildSchematic();
        }
    });

    function selectService(serviceId) {
        if (!serviceId) return;

        serviceDetailPanels.forEach(panel => {
            panel.classList.toggle(
                "is-active",
                panel.dataset.serviceDetail === serviceId
            );
        });

        serviceMenuItems.forEach(item => {
            const isActive = item.dataset.serviceMenu === serviceId;
            item.classList.toggle("is-active", isActive);
            item.setAttribute("aria-current", isActive ? "true" : "false");
        });

        serviceCards.forEach(card => {
            card.setAttribute(
                "aria-expanded",
                card.dataset.service === serviceId &&
                servicesStage?.classList.contains("is-detail-open")
                    ? "true"
                    : "false"
            );
        });
    }

    function openServiceDetail(serviceId, trigger = null) {
        if (!servicesStage || !serviceDetails) return;

        if (trigger) {
            lastServiceTrigger = trigger;
        }

        selectService(serviceId);
        syncServiceStageHeight(serviceDetails);
        servicesStage.classList.add("is-detail-open");
        serviceDetails.setAttribute("aria-hidden", "false");

        serviceCards.forEach(card => {
            card.setAttribute(
                "aria-expanded",
                card.dataset.service === serviceId ? "true" : "false"
            );
        });

        window.setTimeout(() => {
            serviceBack?.focus({ preventScroll: true });
        }, 540);
    }

    function closeServiceDetail() {
        if (!servicesStage || !serviceDetails) return;

        syncServiceStageHeight(servicesOverview);
        servicesStage.classList.remove("is-detail-open");
        serviceDetails.setAttribute("aria-hidden", "true");

        serviceCards.forEach(card => {
            card.setAttribute("aria-expanded", "false");
        });

        const focusTarget = lastServiceTrigger;

        window.setTimeout(() => {
            focusTarget?.focus({ preventScroll: true });
        }, 540);
    }

    serviceCards.forEach(card => {
        card.addEventListener("click", () => {
            openServiceDetail(card.dataset.service, card);
        });
    });

    serviceMenuItems.forEach(item => {
        item.addEventListener("click", () => {
            selectService(item.dataset.serviceMenu);
            requestAnimationFrame(() => {
                syncServiceStageHeight(serviceDetails);
            });
        });
    });

    serviceBack?.addEventListener("click", closeServiceDetail);

    document.addEventListener("keydown", event => {
        if (
            event.key === "Escape" &&
            servicesStage?.classList.contains("is-detail-open")
        ) {
            closeServiceDetail();
        }
    });

    /* =====================================================
       DEVELOPMENT FLOW HOVER
    ===================================================== */

    flowStages.forEach((stage, index) => {
        stage.addEventListener("mouseenter", () => {
            flowStages.forEach(item => item.classList.remove("flow-neighbor"));

            flowStages[index - 1]?.classList.add("flow-neighbor");
            flowStages[index + 1]?.classList.add("flow-neighbor");
        });

        stage.addEventListener("mouseleave", () => {
            flowStages.forEach(item => item.classList.remove("flow-neighbor"));
        });
    });

    if (testStage && developmentFlow) {
        testStage.addEventListener("mouseenter", () => {
            developmentFlow.classList.add("loop-active");
            buildStage?.classList.add("flow-neighbor");
        });

        testStage.addEventListener("mouseleave", () => {
            developmentFlow.classList.remove("loop-active");
            buildStage?.classList.remove("flow-neighbor");
        });
    }

    /* =====================================================
       LOGO
    ===================================================== */

    logo?.addEventListener("click", event => {
        event.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    /* =====================================================
       MOBILE MENU
    ===================================================== */

    mobileMenuButton?.addEventListener("click", () => {
        mobileLinks?.classList.toggle("open");
    });

    mobileLinks?.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            mobileLinks.classList.remove("open");
        });
    });

    /* =====================================================
       LAYOUT CHANGES ONLY
    ===================================================== */

    window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            syncServiceStageHeight();
            rebuildSchematic();
        }, 140);
    });

    if ("ResizeObserver" in window) {
        const layoutObserver = new ResizeObserver(() => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(rebuildSchematic, 100);
        });

        sections.forEach(section => layoutObserver.observe(section));
    }

    syncServiceStageHeight(servicesOverview);
    rebuildSchematic();

    window.addEventListener("load", () => {
        syncServiceStageHeight();
        rebuildSchematic();
        setTimeout(() => {
            syncServiceStageHeight();
            rebuildSchematic();
        }, 250);
    }, { once: true });
});
