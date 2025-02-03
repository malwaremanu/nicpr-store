const { createApp } = Vue;
const emitter = mitt(); // Create a global event bus

// Function to load and parse component files
async function loadComponent(app, name, file) {
    try {
        const response = await fetch(`components/${file}.html`);
        if (!response.ok) throw new Error(`Failed to load ${file}.html`);
        const text = await response.text();

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = text;

        // Extract <template>
        const templateTag = tempDiv.querySelector("template");
        const template = templateTag ? templateTag.innerHTML.trim() : "";

        // Extract <script>
        const scriptTag = tempDiv.querySelector("script");
        let scriptObj = {};
        if (scriptTag) {
            eval(scriptTag.innerHTML); // Execute the script
            scriptObj = window.__component__ || {}; // Retrieve the exported component
        }

        // Inject global event bus in components
        scriptObj.emitter = emitter;

        // Extract <style> and apply dynamically
        const styleTag = tempDiv.querySelector("style");
        if (styleTag) {
            applyComponentStyle(name, styleTag.innerHTML.trim());
        }

        // Register Vue component dynamically
        app.component(name, {
            template: `<div>${template}</div>`,
            ...scriptObj,
        });

        console.log(`Loaded: ${name}`);
    } catch (error) {
        console.error(`Error loading component ${name}:`, error);
    }
}

// Function to inject styles dynamically
function applyComponentStyle(name, cssContent) {
    let existingStyle = document.querySelector(`#style-${name}`);
    if (existingStyle) existingStyle.remove();

    const styleTag = document.createElement("style");
    styleTag.id = `style-${name}`;
    styleTag.innerHTML = cssContent;
    document.head.appendChild(styleTag);
}

// Create Vue App
const app = createApp({
    data() {
        return {
            currentView: "home-component",
        };
    },
    methods: {
        navigate(view) {
            this.currentView = view;
        },
    },
});

// Load Components Before Mounting Vue
Promise.all([
    loadComponent(app, "header-component", "header"),
    loadComponent(app, "footer-component", "footer"),
    loadComponent(app, "home-component", "home"),
    loadComponent(app, "about-component", "about"),
]).then(() => {
    console.log("All components loaded. Mounting Vue...");
    app.config.globalProperties.emitter = emitter; // Make emitter available globally
    app.mount("#app");
}).catch(error => {
    console.error("Failed to load all components:", error);
});
