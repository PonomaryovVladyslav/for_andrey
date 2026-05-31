(function () {
    "use strict";

    const root = document.documentElement;

    // ----- Theme toggle (persisted) -----
    function applyThemeIcon() {
        const btn = document.getElementById("themeToggle");
        if (!btn) return;
        const dark = root.getAttribute("data-theme") === "dark";
        btn.textContent = dark ? "☀️" : "🌙";
        btn.setAttribute("title", dark ? "Светлая тема" : "Тёмная тема");
    }

    function toggleTheme() {
        const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        try { localStorage.setItem("theme", next); } catch (e) {}
        applyThemeIcon();
    }

    // ----- Mobile nav -----
    function toggleNav() {
        const links = document.getElementById("navLinks");
        if (links) links.classList.toggle("open");
    }

    // ----- Active nav link -----
    function highlightNav() {
        const here = window.location.pathname;
        document.querySelectorAll(".nav-links > a").forEach(function (a) {
            const href = a.getAttribute("href");
            if (href === here || (href !== "/" && here.indexOf(href) === 0)) {
                a.classList.add("active");
            }
        });
    }

    // ----- Scroll reveal -----
    function setupReveal() {
        const items = document.querySelectorAll(".reveal");
        if (!("IntersectionObserver" in window)) {
            items.forEach(function (el) { el.classList.add("visible"); });
            return;
        }
        const obs = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        items.forEach(function (el, i) {
            el.style.transitionDelay = Math.min(i * 60, 360) + "ms";
            obs.observe(el);
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        applyThemeIcon();
        highlightNav();
        setupReveal();

        const themeBtn = document.getElementById("themeToggle");
        if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

        const navBtn = document.getElementById("navToggle");
        if (navBtn) navBtn.addEventListener("click", toggleNav);
    });
})();
