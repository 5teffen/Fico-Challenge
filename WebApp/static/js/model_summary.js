function draw_summary(elem) {

    var svg = d3.select(elem).append("svg")
            .attr("width",250)
            .attr("height",500)
            .style("background-color", "#87959e");

    
    const centre = 250/2
    
    svg.append('defs')
      .append('pattern')
        .attr('id', 'diagonalHatch')
        .attr('patternUnits', 'userSpaceOnUse')
        .attr('width', 8)
        .attr('height', 8)
      .append('path')
        .attr('d', 'M-2,2 l4,-4 M0,8 l8,-8 M6,10 l4,-4')
        .attr('stroke', '#000000')
        .attr('stroke-width', 1);
    

    svg.append('g').append("text")
        .text("Model Summary")
        .attr("x",centre)
        .attr("y",50)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
//        .attr("font-weight", "bold")
        .attr("font-size", '22px')
        .attr("fill","white");
    
    
    svg.append('g').append("text")
        .text("SVM Model")
//        .text("Linear Kernel")
        .attr("x",centre)
        .attr("y",80)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '16px')
        .attr("fill","white");
    

        svg.append('g').append("text")
        .text("Linear Kernel")
        .attr("x",centre)
        .attr("y",100)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '16px')
        .attr("fill","white");
    
    
    svg.append('g').append("text")
        .text("Accuracy: 74.8% ")
        .attr("x",centre)
        .attr("y",140)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '16px')
        .attr("fill","white");
    

    svg.append('g').append("rect")
          .attr("x", centre-47)
          .attr("y", 160)
          .attr("width", 45)
          .attr("height", 30)
          .style("fill",'#1b9e77');
    
    svg.append('g').append("rect")
          .attr("x", centre-47)
          .attr("y", 160)
          .attr("width", 45)
          .attr("height", 30)
          .style("fill",'#1b9e77');
    

    svg.append('g').append("rect")
          .attr("x", centre)
          .attr("y", 160)
          .attr("width", 45)
          .attr("height", 30)
          .style("fill",'#1b9e77');

    svg.append('g').append("rect")
        .attr("x", centre)
        .attr("y", 160)
        .attr("width", 45)
        .attr("height", 30)
        .attr("fill", 'url(#diagonalHatch)');
    
    svg.append('g').append("text")
        .text("3282")
        .attr("x",centre-23)
        .attr("y",180)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '14px')
        .attr("fill","white");
    
        
    svg.append('g').append("text")
        .text("1220")
        .attr("x",centre+22)
        .attr("y",180)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '14px')
        .attr("fill","white");

    
    
    
    svg.append('g').append("rect")
          .attr("x", centre-47)
          .attr("y", 192)
          .attr("width", 45)
          .attr("height", 30)
          .style("fill",'#d95f02');

    

    svg.append('g').append("rect")
          .attr("x", centre)
          .attr("y", 192)
          .attr("width", 45)
          .attr("height", 30)
          .style("fill",'#d95f02');

    
    svg.append("rect")
        .attr("x", centre-47)
        .attr("y", 192)
        .attr("width", 45)
        .attr("height", 30)
        .attr("fill", 'url(#diagonalHatch)');
    
    
        svg.append('g').append("text")
        .text("2041")
        .attr("x",centre-23)
        .attr("y",212)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '14px')
        .attr("fill","white");
    
        
    svg.append('g').append("text")
        .text("3916")
        .attr("x",centre+22)
        .attr("y",212)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '14px')
        .attr("fill","white");
    

    
    svg.append('g').append("text")
        .text("Samples with:")
        .attr("x",centre)
        .attr("y",300)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '17px')
        .attr("fill","white");
    
    
    svg.append('g').append("text")
        .text("- Key Features: 7468")
        .attr("x",centre)
        .attr("y",330)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '15px')
        .attr("fill","white");
    
    
    
    svg.append('g').append("text")
        .text("- Changes: 3964")
        .attr("x",centre)
        .attr("y",350)
        .attr("text-anchor","middle")
        .attr("font-family", "sans-serif")
        .attr("font-size", '15px')
        .attr("fill","white");
    
    
    
    
}

