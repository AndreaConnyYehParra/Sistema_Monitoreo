
function crearGraficaDispositivos(pct_normales, pct_advertencias, pct_criticos) {
    const ctx = document.getElementById('distribucion_dispositivos');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Normal', 'Advertencia', 'Crítico'],
            datasets: [{
                data: [pct_normales, pct_advertencias, pct_criticos],
                label: 'Porcentaje (%)',
                backgroundColor: ['#00A2EF', '#F0E300','#F00533',]
            }]
        },
        options: {
    indexAxis: 'y',
    scales: {
        x: {
            max: 100,
            ticks: {
                callback: value => value + '%'
            },
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        },
        y: {
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        }
    },
    plugins: {
        legend: {
            labels: {
                usePointStyle: true,
                pointStyle: 'line'
            }
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.raw;
                    return `${context.label}: ${value.toFixed(1)}%`;
                }
            }
        }
    }
}
    });
}


function crearGraficaDisponibilidad(pct_disponibilidad, pct_nodisponibilidad) {
    const ctx = document.getElementById('disponibilidad_general');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Disponible', 'No Disponible'],
            datasets: [{
                data: [pct_disponibilidad, pct_nodisponibilidad],
                label: 'Porcentaje (%)',
                backgroundColor: ['#00A2EF', '#F00533']
            }]
        },
        options: {
    indexAxis: 'y',
    scales: {
        x: {
            max: 100,
            ticks: {
                callback: value => value + '%'
            },
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        },
        y: {
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        }
    },
    plugins: {
        legend: {
            labels: {
                usePointStyle: true,
                pointStyle: 'line'
            }
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.raw;
                    return `${context.label}: ${value.toFixed(1)}%`;
                }
            }
        }
    }
}
    });
}

function crearGraficaLatencia(tipos, latencias) {
    const ctx = document.getElementById('latencia_promedio');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: tipos,
            datasets: [{
                data: latencias,
                label: 'Latencia Promedio (ms)',
                backgroundColor: ['#0278A3', '#02AEEF']
            }]
        },
        options: {
    responsive: true,
     indexAxis: 'y',
    scales: {
        x: {
            beginAtZero: true,
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        },
        y: {
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        }
    },
    plugins: {
        legend: {
            labels: {
                usePointStyle: true,
                pointStyle: 'line'
            }
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.raw;
                    return `${context.label}: ${value.toFixed(1)} ms`;
                }
            }
        }
    }
}
    });
}

function crearGraficaPaquetes(tipos, perdidas) {
    const ctx = document.getElementById('perdidas_promedio');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: tipos,
            datasets: [{
                data: perdidas,
                label: 'Perdida de Paquetes (%)',
                backgroundColor: ['#0278A3', '#02AEEF']
            }]
        },
        options: {
    responsive: true,
        indexAxis: 'y',
    scales: {
        x: {
            max: 100,
            ticks: {
                callback: value => value + '%'
            },
            beginAtZero: true,
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        },
        y: {
            grid: {
            color: 'rgba(0,0,0,0.05)'
        }
        }
    },
    plugins: {
        legend: {
            labels: {
                usePointStyle: true,
                pointStyle: 'line'
            }
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.raw;
                    return `${context.label}: ${value.toFixed(1)} %`;
                }
            }
        }
    }
}
    });
}