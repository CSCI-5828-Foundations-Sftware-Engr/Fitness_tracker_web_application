import {
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    Line,
    ComposedChart,
} from "recharts";

const Chart = props => {
    const chartData = props.data;
    return (
        <>

            <div className="chart-container">
                <h2>{props.label}</h2>
                <ComposedChart
                    width={350}
                    height={300}
                    data={chartData.data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey={chartData.xAxisDataKey} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar barSize={20} dataKey={chartData.barChartDataKey} name={chartData.barChartName} fill="rgba(34, 193, 195, 1)" />
                    <Line
                        dot={false}
                        strokeWidth={2}
                        strokeLinecap="round"
                        type="monotone"
                        dataKey={chartData.lineChartDataKey}
                        stroke="#ff9900"
                        legendType="rect"
                        name={chartData.lineChartName}
                    />
                </ComposedChart>
            </div>
        </>
    );
}

export default Chart;