document.addEventListener("DOMContentLoaded", () => {

    const body = document.body;
    const dockSentinel = document.getElementById("dockSentinel");
    const mobileMenuButton = document.getElementById("mobileMenuButton");
    const mobileLinks = document.getElementById("mobileLinks");
    const revealItems = Array.from(document.querySelectorAll(".reveal-on-scroll"));
    const projectPosts = Array.from(document.querySelectorAll(".portfolio-post"));


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
       MOBILE MENU
    ===================================================== */

    if (mobileMenuButton && mobileLinks) {
        mobileMenuButton.addEventListener("click", () => {
            const isOpen = mobileLinks.classList.toggle("open");
            mobileMenuButton.setAttribute("aria-expanded", String(isOpen));
        });

        mobileLinks.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", () => {
                mobileLinks.classList.remove("open");
                mobileMenuButton.setAttribute("aria-expanded", "false");
            });
        });
    }


    /* =====================================================
       CHEAP SCROLL REVEAL

       IntersectionObserver only changes classes when the
       element enters the viewport. No continuous scroll math.
    ===================================================== */

    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            entries => {
                entries.forEach(entry => {
                    if (!entry.isIntersecting) return;

                    entry.target.classList.add("is-visible");
                    revealObserver.unobserve(entry.target);
                });
            },
            {
                root: null,
                rootMargin: "0px 0px -12% 0px",
                threshold: .08
            }
        );

        revealItems.forEach(item => revealObserver.observe(item));
    } else {
        revealItems.forEach(item => item.classList.add("is-visible"));
    }


    /* =====================================================
       PORTFOLIO POST DETAILS
    ===================================================== */

    projectPosts.forEach(post => {
        const toggle = post.querySelector(".post-toggle");
        const details = post.querySelector(".post-details");

        if (!toggle || !details) return;

        toggle.addEventListener("click", () => {
            const isOpen = post.classList.toggle("is-open");

            toggle.setAttribute("aria-expanded", String(isOpen));
            details.setAttribute("aria-hidden", String(!isOpen));

            const label = toggle.childNodes[0];
            if (label) {
                label.nodeValue = isOpen
                    ? "Hide project notes "
                    : "View project notes ";
            }
        });
    });

});
