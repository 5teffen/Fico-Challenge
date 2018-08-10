function draw_graph(testData, densityData, result){

    console.log(testData)
    console.log(densityData)

    var good_col = "#1b9e77",
        bad_col = "#d95f02";

    var the_colour = "";
    var opp_colour = "";
    
    var separator = 0.015;
    
    if (result) {
        opp_colour = good_col;
        the_colour = bad_col;}
    else {
        opp_colour = bad_col
        the_colour = good_col;}
    
    // -- Establishing margins and canvas bounds -- 
    var margin = {
            top: 10, 
            right: 60, 
            bottom: 140, 
            left: 70
        },
        width = 1000 - margin.right - margin.left,
        height = 360 - margin.top - margin.bottom;

    var padding_top = 0.2,
        padding_bottom = 0.1;

    var outlier = 1 + padding_top/2;
    
    // -- Adding scales based on canvas -- 
    var xScale = d3.scaleBand()
            .domain(testData.map(function(d){return d.name;}))
            .rangeRound([0, width])
            .paddingInner(separator),
        yScale = d3.scaleLinear()
            .domain([0-padding_bottom, 1+padding_top])
            .rangeRound([height, 0]);

    var svg = d3.select(".d3-space")
                .append("svg")
                .attr("width",width + margin.right + margin.left)
                .attr("height",height + margin.top + margin.bottom)
                .attr("class", "main-svg")
                .append("g")
                     .attr("transform","translate(" + margin.left + ',' + margin.top +')');

    // -- Drawing background rectangles -- 
    svg.selectAll("rect")
        .data(testData)
        .enter()
        .append("rect")
        .attr("class","bg_bar")
        .attr('x',function(d) {return xScale(d.name);})
        .attr('y',0)
        .attr("height",function(d){return yScale(0-padding_bottom)})
        .attr("width",xScale.bandwidth())
        .style("opacity",function(d){
            if(d.anch == 1){
                return 0.2;
            }
            else {return 1;}
        })
        .style("fill",function(d){
            if(d.anch == 1){
                return opp_colour;
            }
            else {return "white";}
        });
    
    
    // -- Drawing dividing lines -- 
    svg.selectAll("line")
        .data(testData)
        .enter()
        .append("line")
        .attr("class","split_lines")
        .attr("x1",function(d) {return xScale(d.name)+xScale.bandwidth();})
        .attr('y',0)
        .attr("y2",function(d){return yScale(0-padding_bottom)})
        .attr("x2",function(d) {return xScale(d.name)+xScale.bandwidth();})
        .style("stroke",function(d,i){
            if (i == testData.length-1) {return "None";}
            else {return "#A9A9A9";}})
        .style("stroke-width",0.7);
    
    // -- Drawing surrounding box -- 
        svg.append("rect")
        .attr("class","border")
        .attr('x',xScale(testData[0].name))
        .attr('y',0)
        .attr("height",function(d){return yScale(0-padding_bottom)})
        .attr("width",(xScale.bandwidth()+1)*testData.length)
        .attr("fill","None")
        .attr("stroke","#A9A9A9")
        .attr("stroke-width",1);

    function draw_density_boxed(testData,data) {
        console.log("Getting Called");
        var overlap = yScale(0.1)-yScale(0.2);

        for (ind=0 ; ind < data.length; ind++) {
            var cur_obj = data[ind];
            var array_len = Object.keys(cur_obj).length;

            for (n=0 ; n < array_len; ++n){
                var key = Object.keys(cur_obj)[n];
                var value = cur_obj[key];
                
                svg.append("g")
                .append("rect")
                .attr('x',function() {return xScale(testData[ind].name)})
                .attr('y',function() {
                        return yScale(+key)-overlap;})
                .attr("height",2*overlap)
                .attr("width",xScale.bandwidth())
                .style("stroke","black")
                .style("stroke-width",0.15)
                .style("opacity",function(){return value/9800})
                .style("fill","#7570b3");
            }
                
        }
    }
    
    function draw_density_gradient(testData,data) {
        var defs = svg.append("defs");
        var linearGradient = defs.append("linearGradient")
           .attr("id", "lin_fill")
           .attr("x1", "0%")
           .attr("x2", "0%")
           .attr("y1", "0%")
           .attr("y2", "100%");
    
        var colorScale = d3.scaleLinear()
            .range(["#dfdeed","#7570b3", "#dfdeed"]);

        linearGradient.selectAll("stop")
            .data(colorScale.range() )
            .enter().append("stop")
            .attr("offset", function(d,i) { return i/(colorScale.range().length-1); })
            .attr("stop-color", function(d) { return d; });

        
        console.log("Getting Called");
        var overlap = yScale(0.1)-yScale(0.2);

        for (ind=0 ; ind < data.length; ind++) {
            var cur_obj = data[ind];
            var array_len = Object.keys(cur_obj).length;

            for (n=0 ; n < array_len; ++n){
                var key = Object.keys(cur_obj)[n];
                var value = cur_obj[key];
                
                svg.append("g")
                .append("rect")
                .attr('x',function() {return xScale(testData[ind].name)})
                .attr('y',function() {
                        return yScale(+key)-overlap;})
                .attr("height",2*overlap)
                .attr("width",xScale.bandwidth())
                .style("opacity",function(){return value/7000})
                .style("fill","url(#lin_fill)");
            }
                
        }
    }
    
    
    // if (densityData != "no"){ draw_density_boxed(testData, densityData);}
   if (densityData != "no"){ draw_density_gradient(testData, densityData);}
    
    
    
    function draw_polygons(data) {
        var full_string = "";
        var mod = 2 // To fix the sizes for some cases
        
        var bar_len = 0.085
        var separation = 0.015

        for(n=0 ; n < data.length; n++){
            var d = data[n];
            if (d.scl_val > 1) {new_val = 1;}
            else {new_val = d.scl_val;}

            if (d.scl_val > d.scl_change){

                var start_x = (xScale(d.name) + xScale.bandwidth()*0.35).toString();
                var mid_x = (xScale(d.name) + xScale.bandwidth()*0.5).toString();
                var end_x = (xScale(d.name) + xScale.bandwidth()*0.65).toString();

                var start_y = (yScale(new_val)).toString();
                var bottom_mid = (yScale(new_val)+5).toString();
                var end_mid = (yScale(new_val-bar_len)+5).toString();
                var end_y = (yScale(new_val-bar_len)).toString();

                full_string += "M"+start_x+","+start_y+"L"+end_x+","+start_y+"L"+end_x+","+end_y
                +"L"+mid_x+","+end_mid+"L"+start_x+","+end_y+"L"+start_x+","+start_y;
                var shift = bar_len+separation;

                for(i=1 ; i < d.incr; i++){
                            start_y = (yScale(new_val-shift)).toString(); 
                            bottom_mid = (yScale(new_val-shift)+5).toString();
                            end_mid = (yScale(new_val-bar_len-shift)+5).toString();
                            end_y = (yScale(new_val-bar_len-shift)).toString();

                        var next_pol = "M"+start_x+","+start_y+"L"+mid_x+","+bottom_mid+"L"+end_x+","+start_y+"L"+end_x+","+end_y
                            +"L"+mid_x+","+end_mid+"L"+start_x+","+end_y+"L"+start_x+","+start_y; 


                        full_string += next_pol;
                        shift += bar_len+separation;
                    }
                }

            else if (d.scl_val < d.scl_change){

                var start_x = (xScale(d.name) + xScale.bandwidth()*0.35).toString();
                var mid_x = (xScale(d.name) + xScale.bandwidth()*0.5).toString();
                var end_x = (xScale(d.name) + xScale.bandwidth()*0.65).toString();

                var start_y = (yScale(new_val)).toString();
                var bottom_mid = (yScale(new_val)-5).toString();
                var end_mid = (yScale(new_val+bar_len)-5).toString();
                var end_y = (yScale(new_val+bar_len)).toString();
        

                full_string += "M"+start_x+","+start_y+"L"+end_x+","+start_y+"L"+end_x+","+end_y
                +"L"+mid_x+","+end_mid+"L"+start_x+","+end_y+"L"+start_x+","+start_y;

                var shift = bar_len+separation;

                for(i=1 ; i < d.incr; i++){
                            start_y = (yScale(new_val+shift)).toString();
                            bottom_mid = (yScale(new_val+shift)-5).toString();
                            end_mid = (yScale(new_val+bar_len+shift)-5).toString();
                            end_y = (yScale(new_val+bar_len+shift)).toString();

                        var next_pol = "M"+start_x+","+start_y+"L"+mid_x+","+bottom_mid+"L"+end_x+","+start_y+"L"+end_x+","+end_y
                            +"L"+mid_x+","+end_mid+"L"+start_x+","+end_y+"L"+start_x+","+start_y; 


                        full_string += next_pol;
                        shift += bar_len+separation;

                    }
                }
            }




            return full_string;
    }

    svg.append("path")
        .attr('d',draw_polygons(testData))
        .attr("fill",the_colour)
        .attr("stroke",the_colour)
        .attr("stroke-linecap","round")
        .attr("stroke-width",0);


    svg.append("g")
        .selectAll('text')
        .data(testData)
        .enter()
        .append('text')
        .text(function(d){return d.change;})
        .attr("x", function(d){return xScale(d.name) + xScale.bandwidth()/2})
        .attr("y", function(d){
            if (d.change >= d.val){
                return yScale(d.scl_val+d.incr*0.10)-5;
            }
            else {
                if (d.scl_val > 1){return yScale(1-d.incr*0.10)+12;}
                else {return yScale(d.scl_val-d.incr*0.10)+12;}
            }
        })
        .attr("font-family", 'sans-serif')
        .attr("font-size", '12px')
        .attr("font-weight", 'bold')
        .attr("fill", function(d) {
            if ((d.change != d.val)) {return the_colour;}
            else {return "None"}})
        .attr("text-anchor",'middle');

    
    // -- Handling the special case --
    svg.append("g")
        .selectAll("rect")
        .data(testData.filter(function(d){return (d.scl_val > 1)&&(d.scl_val != d.scl_change);}))
        .enter()
        .append("rect")
        .attr("class","special")
        .attr('x',function(d) {return xScale(d.name)+ xScale.bandwidth()*0.35-1;})
        .attr('y',function(d) {return yScale(outlier);})
        .attr("height",function(d){return yScale(1)-yScale(outlier)+1;})
        .attr("width",xScale.bandwidth()*0.3+2)
        .attr("fill",the_colour)
        .attr("stroke-width",2)
        .style("stroke",function(d){
            if(d.anch == 1){
                if (result == 0){return "#f5e0d4";}
                else {return "#daebe4";}
            }
            else {return "white";}
        });

    svg.append("g")
        .selectAll("circle")
        .data(testData.filter(function(d){return (d.scl_val > 1)&&(d.scl_val != d.scl_change);}))
        .enter()
        .append("circle")
        .attr("r",1.5)
        .attr("cy",function(d) {return yScale(outlier-padding_top/8);})
        .attr("cx",function(d) {return xScale(d.name)+xScale.bandwidth()*0.5;})
        .attr("fill","white");

    svg.append("g")
        .selectAll("circle")
        .data(testData.filter(function(d){return (d.scl_val > 1)&&(d.scl_val != d.scl_change);}))
        .enter()
        .append("circle")
        .attr("r",1.5)
        .attr("cy",function(d) {return yScale(outlier-padding_top/4);})
        .attr("cx",function(d) {return xScale(d.name)+xScale.bandwidth()*0.5;})
        .attr("fill","white");

    svg.append("g")
        .selectAll("circle")
        .data(testData.filter(function(d){return (d.scl_val > 1)&&(d.scl_val != d.scl_change);}))
        .enter()
        .append("circle")
        .attr("r",1.5)
        .attr("cy",function(d) {return yScale(outlier-padding_top*3/8);})
        .attr("cx",function(d) {return xScale(d.name)+xScale.bandwidth()*0.5;})
        .attr("fill","white");
    

    // -- Drawing and styling the AXIS
    
    var xAxis = d3.axisBottom().scale(xScale);

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")  
            .style("fill","black")
            .style("text-anchor", "end")
            .attr("dy", "0.5em")
            .attr("dx", "-0.5em")
            .attr("transform","rotate(-40)");

    // -- Drawing the initial level (blue) --
    svg.append("g")
        .selectAll("line")
        .data(testData)
        .enter()
        .append("line")
        .attr("class","line_lvl")
        .attr("x1",function(d){return xScale(d.name) + xScale.bandwidth()*0.25})
        .attr("x2",function(d){return xScale(d.name) + xScale.bandwidth()*0.75})
        .attr("y1",function(d){
            if (d.scl_val > 1){
                return yScale(outlier)-1}
            else{
                return yScale(d.scl_val)
            }})
        .attr("y2",function(d){
            if (d.scl_val > 1){
                return yScale(outlier)-1}
            else{
                return yScale(d.scl_val)
            }})
        .attr("stroke", "black")
        .attr("stroke-width", 4)
        .attr("stroke-linecap","round")
        .attr("fill", "none");



    // -- The text for initial level (blue) --
    svg.append("g")
        .selectAll('text')
        .data(testData)
        .enter()
        .append('text')
        .text(function(d){return d.val;})
        .attr("x", function(d){return xScale(d.name) + xScale.bandwidth()/2})
        .attr("y", function(d){
            if (d.scl_val > 1){
                return yScale(outlier)-4;
            }

            if (d.change >= d.val){
                return yScale(d.scl_val)+12;
            }

            else {
                return yScale(d.scl_val)-3;
            }
        })
        .attr("font-family", 'sans-serif')
        .attr("font-size", '12px')
        .attr("font-weight", 'bold')
        .attr("fill",'black')
        .attr("text-anchor",'middle');


    function wrap(text, width) {
      text.each(function() {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            y = text.attr("y"),
            dy = parseFloat(text.attr("dy")),
            tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(" "));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
          }
        }
      });
    }
}
