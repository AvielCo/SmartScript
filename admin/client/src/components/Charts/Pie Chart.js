import React, { Component } from 'react';
import CanvasJSReact from './canvasjs.react';
import './PieChart.css'
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
 
function PieChart({text,dataPoints})  {
	
	const options = {
    theme: "dark",
    animationEnabled: true,
    title: {
      text,
    },
    data: [
      {
        type: "pie",
        showInLegend: true,
        legendText: "{label}",
        toolTipContent: "{label}: <strong>{y}</strong>",
        indexLabel: "{p}%",
        indexLabelPlacement: "inside",
        dataPoints,
      },
    ],
  };
		
		return (
		<div>
			<CanvasJSChart options = {options} />
		</div>
		);
	}



export default PieChart;