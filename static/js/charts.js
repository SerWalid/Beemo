window.addEventListener("load", () => {
  async function fetchInteractionData() {
    try {
      const response = await fetch("/get-interaction-last-7-days");
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching interaction data:", error);
      return [];
    }
  }
  (async function () {
    // Fetch the interaction data
    const interactionData = await fetchInteractionData();

    // Process the data to extract dates and interaction counts
    const categories = interactionData.map((item) => item.date); // Extract dates
    const interactionCounts = interactionData.map(
      (item) => item.number_of_interaction
    ); // Extract interaction counts
    buildChart(
      "#hs-single-area-chart",
      (mode) => ({
        chart: {
          height: 300,
          type: "area",
          toolbar: {
            show: false,
          },
          zoom: {
            enabled: false,
          },
        },
        series: [
          {
            name: "Interactions",
            data: interactionCounts,
          },
        ],
        legend: {
          show: false,
        },
        dataLabels: {
          enabled: false,
        },
        stroke: {
          curve: "straight",
          width: 2,
        },
        grid: {
          strokeDashArray: 2,
        },
        fill: {
          type: "gradient",
          gradient: {
            type: "vertical",
            shadeIntensity: 1,
            opacityFrom: 0.1,
            opacityTo: 0.8,
          },
        },
        xaxis: {
          type: "category",
          tickPlacement: "on",
          categories: categories,
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
          crosshairs: {
            stroke: {
              dashArray: 0,
            },
            dropShadow: {
              show: false,
            },
          },
          tooltip: {
            enabled: false,
          },
          labels: {
            style: {
              colors: "#9ca3af",
              fontSize: "13px",
              fontWeight: 400,
            },
            formatter: (title) => {
              let t = title;

              if (t) {
                const newT = t.split(" ");
                t = `${newT[0]} ${newT[1].slice(0, 3)}`;
              }

              return t;
            },
          },
        },
        yaxis: {
          labels: {
            align: "left",
            minWidth: 0,
            maxWidth: 140,
            style: {
              colors: "#9ca3af",
              fontSize: "13px",
              fontFamily: "Inter, ui-sans-serif",
              fontWeight: 400,
            },
            formatter: (value) => (value >= 1000 ? `${value / 1000}k` : value),
          },
        },
        tooltip: {
          x: {
            format: "MMMM yyyy",
          },
          y: {
            formatter: (value) =>
              `${value >= 1000 ? `${value / 1000}k` : value}`,
          },
          custom: function (props) {
            const { categories } = props.ctx.opts.xaxis;
            const { dataPointIndex } = props;
            const title = categories[dataPointIndex].split(" ");
            const newTitle = `${title[0]} ${title[1]}`;

            return buildTooltip(props, {
              title: newTitle,
              mode,
              valuePrefix: "",
              hasTextLabel: true,
              markerExtClasses: "!rounded-sm",
              wrapperExtClasses: "min-w-28",
            });
          },
        },
        responsive: [
          {
            breakpoint: 568,
            options: {
              chart: {
                height: 300,
              },
              labels: {
                style: {
                  colors: "#9ca3af",
                  fontSize: "11px",
                  fontFamily: "Inter, ui-sans-serif",
                  fontWeight: 400,
                },
                offsetX: -2,
                formatter: (title) => title.slice(0, 3),
              },
              yaxis: {
                labels: {
                  align: "left",
                  minWidth: 0,
                  maxWidth: 140,
                  style: {
                    colors: "#9ca3af",
                    fontSize: "11px",
                    fontFamily: "Inter, ui-sans-serif",
                    fontWeight: 400,
                  },
                  formatter: (value) =>
                    value >= 1000 ? `${value / 1000}k` : value,
                },
              },
            },
          },
        ],
      }),
      {
        colors: ["#2563eb", "#9333ea"],
        fill: {
          gradient: {
            stops: [0, 90, 100],
          },
        },
        grid: {
          borderColor: "#e5e7eb",
        },
      },
      {
        colors: ["#3b82f6", "#a855f7"],
        fill: {
          gradient: {
            stops: [100, 90, 0],
          },
        },
        grid: {
          borderColor: "#404040",
        },
      }
    );
  })();
});
