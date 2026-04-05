/**
 * China Heavy Metals Dashboard - Main Logic
 */

document.addEventListener('DOMContentLoaded', async () => {
    const mapElement = document.getElementById('plotly-map');
    const loadingOverlay = document.querySelector('.loading-overlay');
    const buttons = document.querySelectorAll('.layer-btn');

    try {
        // 1. Fetch pre-computed map data
        const response = await fetch('map_data.json');
        if (!response.ok) throw new Error('Could not load map data.');
        const mapData = await response.json();

        // 2. Initialize the plot
        // The JSON contains data and layout. We preserve them.
        const data = mapData.data;
        const layout = mapData.layout;

        // Custom responsive config
        const config = {
            responsive: true,
            displayModeBar: false,
        };

        // Create the plot
        await Plotly.newPlot(mapElement, data, layout, config);

        // Hide overlay once rendered
        loadingOverlay.style.opacity = '0';
        setTimeout(() => loadingOverlay.style.display = 'none', 500);

        // 3. Setup Custom Layer Toggles
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const layerType = btn.getAttribute('data-layer');
                
                // Update button UI
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Determine visibility for traces
                // Trace Mapping from export script:
                // 0: Pb Grid
                // 1: Cd Grid
                // 2: Hg Grid
                // 3: Overall Grid
                // 4,5,6: Station points (always visible or toggle group)
                
let visibility;
                switch(layerType) {
                    case 'overall':
                        // Show: Overall Grid [3] and Overall Stations [7]
                        visibility = [false, false, false, true, false, false, false, true];
                        break;
                    case 'pb':
                        // Show: Pb Grid [0] and Pb Stations [4]
                        visibility = [true, false, false, false, true, false, false, false];
                        break;
                    case 'cd':
                        // Show: Cd Grid [1] and Cd Stations [5]
                        visibility = [false, true, false, false, false, true, false, false];
                        break;
                    case 'hg':
                        // Show: Hg Grid [2] and Hg Stations [6]
                        visibility = [false, false, true, false, false, false, true, false];
                        break;
                    case 'none':
                        // Hide all grids, show only the Overall Stations [7]
                        visibility = [false, false, false, false, false, false, false, true];
                        break;
                }

                // Apply update to Plotly
                Plotly.restyle(mapElement, { 'visible': visibility });
            });
        });

    } catch (err) {
        console.error(err);
        loadingOverlay.innerHTML = `<p style="color: #ff3300">Error: ${err.message}</p>`;
    }
});
