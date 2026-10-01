// Job Market Intelligence - Dark Theme Chart.js Initializers & Styling

const DarkChartTheme = {
  fontFamily: "'Plus Jakarta Sans', sans-serif",
  textColor: '#94a3b8',
  gridColor: 'rgba(255, 255, 255, 0.05)',
  borderColor: 'rgba(255, 255, 255, 0.1)',
  colors: {
    primary: '#6366f1',
    secondary: '#06b6d4',
    emerald: '#10b981',
    amber: '#f59e0b',
    rose: '#f43f5e',
    purple: '#a855f7',
    blue: '#3b82f6',
    slate: '#475569',
  },
  palette: [
    '#6366f1', '#06b6d4', '#10b981', '#f59e0b',
    '#ec4899', '#8b5cf6', '#3b82f6', '#14b8a6',
    '#f97316', '#a855f7'
  ]
};

// Global Chart.js Defaults
if (typeof Chart !== 'undefined') {
  Chart.defaults.font.family = DarkChartTheme.fontFamily;
  Chart.defaults.color = DarkChartTheme.textColor;
  Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.92)';
  Chart.defaults.plugins.tooltip.titleColor = '#f8fafc';
  Chart.defaults.plugins.tooltip.bodyColor = '#cbd5e1';
  Chart.defaults.plugins.tooltip.borderColor = 'rgba(99, 102, 241, 0.3)';
  Chart.defaults.plugins.tooltip.borderWidth = 1;
  Chart.defaults.plugins.tooltip.padding = 12;
  Chart.defaults.plugins.tooltip.cornerRadius = 10;
  Chart.defaults.plugins.tooltip.boxPadding = 6;
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.legend.labels.boxWidth = 8;
}

// Chart Initializers
function createBarChart(canvasId, labels, data, labelName = 'Count', color = '#6366f1', horizontal = false) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: labelName,
        data: data,
        backgroundColor: color,
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: horizontal ? 'y' : 'x',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { color: DarkChartTheme.gridColor, drawBorder: false },
          ticks: { color: DarkChartTheme.textColor }
        },
        y: {
          grid: { color: DarkChartTheme.gridColor, drawBorder: false },
          ticks: { color: DarkChartTheme.textColor }
        }
      }
    }
  });
}

function createDoughnutChart(canvasId, labels, data, colors = DarkChartTheme.palette) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderWidth: 2,
        borderColor: '#0f172a',
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: DarkChartTheme.textColor,
            padding: 16,
            font: { size: 11 }
          }
        }
      }
    }
  });
}

function createLineChart(canvasId, labels, data, labelName = 'Trend', color = '#06b6d4', fill = true) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: labelName,
        data: data,
        borderColor: color,
        backgroundColor: fill ? 'rgba(6, 182, 212, 0.12)' : 'transparent',
        borderWidth: 3,
        pointBackgroundColor: color,
        pointBorderColor: '#0f172a',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        tension: 0.35,
        fill: fill,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { color: DarkChartTheme.gridColor, drawBorder: false },
          ticks: { color: DarkChartTheme.textColor }
        },
        y: {
          grid: { color: DarkChartTheme.gridColor, drawBorder: false },
          ticks: { color: DarkChartTheme.textColor }
        }
      }
    }
  });
}

function createRadarChart(canvasId, labels, data, labelName = 'Skill Match') {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{
        label: labelName,
        data: data,
        backgroundColor: 'rgba(99, 102, 241, 0.25)',
        borderColor: '#6366f1',
        pointBackgroundColor: '#6366f1',
        pointBorderColor: '#ffffff',
        pointHoverBackgroundColor: '#ffffff',
        pointHoverBorderColor: '#6366f1',
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
          grid: { color: 'rgba(255, 255, 255, 0.08)' },
          pointLabels: {
            color: '#cbd5e1',
            font: { size: 11, weight: '500' }
          },
          ticks: {
            backdropColor: 'transparent',
            color: '#64748b',
            showLabelBackdrop: false
          }
        }
      }
    }
  });
}
