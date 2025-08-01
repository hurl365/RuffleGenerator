document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("paramsForm");
    const viewer = document.getElementById("viewer");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const params = new URLSearchParams(new FormData(form));
        const response = await fetch(`/generate-stl?${params.toString()}`);

        if (!response.ok) {
        alert("Failed to generate STL.");
        return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // Load STL with Three.js
        loadSTLToViewer(url);
    });

    async function loadSTLToViewer(url) {
        viewer.innerHTML = ""; // Clear previous render

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, viewer.clientWidth / viewer.clientHeight, 0.1, 1000);
        camera.position.z = 3;

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(viewer.clientWidth, viewer.clientHeight);
        viewer.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);

        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(5, 5, 5).normalize();
        scene.add(light);

        const loader = new THREE.STLLoader();
        loader.load(url, function (geometry) {
        const material = new THREE.MeshStandardMaterial({ color: 0x0077be, metalness: 0.3, roughness: 0.6 });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
        animate();
        });

        function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
        }
    }
});