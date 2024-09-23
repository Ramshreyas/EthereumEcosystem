function waitForElements(callback) {
    var interval = setInterval(function() {
        var fsButton = document.getElementById('fullscreen-button');
        var treemapChartContainer = document.getElementById('treemap-chart');

        if (fsButton && treemapChartContainer) {
            // Find the Plotly graph element inside the container
            var treemapChart = treemapChartContainer.querySelector('.js-plotly-plot, .plotly-graph-div');

            if (treemapChart) {
                clearInterval(interval);
                callback(fsButton, treemapChart);
            } else {
                console.error('Treemap chart element not found inside container');
                // For debugging: log the contents of treemapChartContainer
                console.log('treemapChartContainer contents:', treemapChartContainer.innerHTML);
            }
        }
    }, 100);
}

waitForElements(function(fsButton, treemapChart) {
    console.log('Fullscreen button and treemap chart found');
    fsButton.addEventListener('click', function() {
        console.log('Fullscreen button clicked');
        if (document.fullscreenElement) {
            console.log('Exiting fullscreen mode');
            document.exitFullscreen();
        } else {
            console.log('Entering fullscreen mode');
            if (treemapChart.requestFullscreen) {
                treemapChart.requestFullscreen();
            } else if (treemapChart.webkitRequestFullscreen) { /* Safari */
                treemapChart.webkitRequestFullscreen();
            } else if (treemapChart.msRequestFullscreen) { /* IE11 */
                treemapChart.msRequestFullscreen();
            } else {
                console.error('Fullscreen API is not supported');
            }
        }
    });
});
