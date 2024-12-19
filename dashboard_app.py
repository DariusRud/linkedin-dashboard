<!DOCTYPE html>
<html lang="lt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Dashboard</title>
    <!-- Plotly.js -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <!-- Papa Parse CSV parser -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .chart-container {
            transition: all 0.3s ease;
        }
        .chart-container:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow">
        <div class="max-w-7xl mx-auto py-6 px-4">
            <h1 class="text-3xl font-bold text-gray-900">LinkedIn Analytics Dashboard</h1>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 px-4">
        <!-- File Input Section -->
        <div class="mb-8 p-6 bg-white rounded-lg shadow">
            <h2 class="text-xl font-semibold mb-4">Duomenų įkėlimas</h2>
            <input type="file" id="csvFile" accept=".csv,.xlsx" 
                   class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"/>
        </div>

        <!-- KPI Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-600">Bendras Pasiekiamumas</h3>
                <p id="totalReach" class="text-3xl font-bold text-blue-600">-</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-600">Vidutinis Įsitraukimas</h3>
                <p id="avgEngagement" class="text-3xl font-bold text-green-600">-</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-600">Konversijų Skaičius</h3>
                <p id="totalConversions" class="text-3xl font-bold text-purple-600">-</p>
            </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="chart-container bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Pasiekiamumas Laike</h3>
                <div id="reachChart" class="w-full h-64"></div>
            </div>
            <div class="chart-container bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Įsitraukimo Metrika</h3>
                <div id="engagementChart" class="w-full h-64"></div>
            </div>
            <div class="chart-container bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Konversijų Tendencijos</h3>
                <div id="conversionChart" class="w-full h-64"></div>
            </div>
            <div class="chart-container bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Efektyviausios Kampanijos</h3>
                <div id="campaignChart" class="w-full h-64"></div>
            </div>
        </div>
    </main>

    <script>
        // Globalūs kintamieji duomenims
        let chartData = {
            dates: [],
            reach: [],
            engagement: [],
            conversions: []
        };

        // Failų įkėlimo funkcionalumas
        document.getElementById('csvFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                if (file.name.endsWith('.csv')) {
                    Papa.parse(file, {
                        complete: function(results) {
                            processData(results.data);
                        },
                        header: true
                    });
                } else if (file.name.endsWith('.xlsx')) {
                    // TODO: Pridėti Excel failo apdorojimą
                    alert('Excel failų palaikymas bus pridėtas netrukus');
                }
            }
        });

        // Duomenų apdorojimas
        function processData(data) {
            // Išvalome senus duomenis
            chartData = {
                dates: [],
                reach: [],
                engagement: [],
                conversions: []
            };

            // Apdorojame duomenis (pavyzdys)
            data.forEach(row => {
                if (row.Date) {
                    chartData.dates.push(row.Date);
                    chartData.reach.push(parseInt(row.Reach) || 0);
                    chartData.engagement.push(parseInt(row.Engagement) || 0);
                    chartData.conversions.push(parseInt(row.Conversions) || 0);
                }
            });

            updateDashboard();
        }

        // Dashboard'o atnaujinimas
        function updateDashboard() {
            // KPI atnaujinimas
            document.getElementById('totalReach').textContent = 
                chartData.reach.reduce((a, b) => a + b, 0).toLocaleString();
            document.getElementById('avgEngagement').textContent = 
                (chartData.engagement.reduce((a, b) => a + b, 0) / chartData.engagement.length || 0).toFixed(2) + '%';
            document.getElementById('totalConversions').textContent = 
                chartData.conversions.reduce((a, b) => a + b, 0).toLocaleString();

            // Grafikų atnaujinimas
            updateReachChart();
            updateEngagementChart();
            updateConversionChart();
            updateCampaignChart();
        }

        // Grafikų funkcijos
        function updateReachChart() {
            const trace = {
                x: chartData.dates,
                y: chartData.reach,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Pasiekiamumas',
                line: {color: '#3B82F6'}
            };

            const layout = {
                margin: {t: 10, r: 10, b: 40, l: 40},
                showlegend: false,
                xaxis: {showgrid: false},
                yaxis: {showgrid: true, gridcolor: '#E5E7EB'}
            };

            Plotly.newPlot('reachChart', [trace], layout, {responsive: true});
        }

        function updateEngagementChart() {
            const trace = {
                x: chartData.dates,
                y: chartData.engagement,
                type: 'bar',
                name: 'Įsitraukimas',
                marker: {color: '#10B981'}
            };

            const layout = {
                margin: {t: 10, r: 10, b: 40, l: 40},
                showlegend: false,
                xaxis: {showgrid: false},
                yaxis: {showgrid: true, gridcolor: '#E5E7EB'}
            };

            Plotly.newPlot('engagementChart', [trace], layout, {responsive: true});
        }

        function updateConversionChart() {
            const trace = {
                x: chartData.dates,
                y: chartData.conversions,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Konversijos',
                line: {color: '#8B5CF6'}
            };

            const layout = {
                margin: {t: 10, r: 10, b: 40, l: 40},
                showlegend: false,
                xaxis: {showgrid: false},
                yaxis: {showgrid: true, gridcolor: '#E5E7EB'}
            };

            Plotly.newPlot('conversionChart', [trace], layout, {responsive: true});
        }

        function updateCampaignChart() {
            // Sukuriame suvestinę pagal kampanijas (pavyzdys)
            const campaigns = {
                'Kampanija A': Math.random() * 100,
                'Kampanija B': Math.random() * 100,
                'Kampanija C': Math.random() * 100,
                'Kampanija D': Math.random() * 100
            };

            const trace = {
                x: Object.keys(campaigns),
                y: Object.values(campaigns),
                type: 'bar',
                marker: {
                    color: ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B']
                }
            };

            const layout = {
                margin: {t: 10, r: 10, b: 40, l: 40},
                showlegend: false,
                xaxis: {showgrid: false},
                yaxis: {showgrid: true, gridcolor: '#E5E7EB'}
            };

            Plotly.newPlot('campaignChart', [trace], layout, {responsive: true});
        }

        // Pradinis dashboard'o atvaizdavimas
        updateDashboard();
    </script>
</body>
</html>