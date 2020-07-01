function draw_all_anchs(textData, goodData, badData, limit, elemn, idx) {

    const horizontal_limit = limit/2;
    
    const good_col = "#1b9e77",
          bad_col = "#d95f02";
    
    var x1_shift = 0,
        x2_shift = 0,
        y1_shift = 0,
        y2_shift = 0,
        
        x_sep = 4,
        y_sep = 4;
    
    const sq_height = 15,
          sq_width = 15;

    const margin = {
            top: 10, 
            right: 0,
            bottom: 10, 
            left: 0
        };


    var text_shift = 0,
        text_feat = 30,
        text_space = 95;
          
    var width = 420 - margin.right - margin.left - text_space,
        height = 100 - margin.top - margin.bottom;

    var svg = d3.select(elemn)
        .append("svg")
        .attr("class", "middle-svg")
        .attr("id", "middle-section-"+idx.toString())
        .attr("width",width + margin.right + margin.left + text_space)
        .attr("height",height + margin.top + margin.bottom)
            .append("g")
                .attr("transform","translate(" + margin.left + ',' + margin.top +')');
    
    for (i = 0; i < textData.length; ++i){
        var name_string = (textData[i].name).toString();
        var label_string = "Ft." + (textData[i].label).toString();
        
        svg.append('g').append("text")
            .text(name_string)
            .attr("x",text_feat)
            .attr("y",10+text_shift)  
            .attr("font-family", 'sans-serif')
            .attr("font-size", '10px')
            .attr("fill","#808080")
            .attr("text-anchor",'start')
                .call(wrap, text_space);

                
        svg.append('g').append("text")
            .text(label_string)
            .attr("x",0)
            .attr("y",10+text_shift)
            .attr("font-family", 'sans-serif')
            .attr("font-size", '12px')
            .attr("fill","#808080")
            .attr("text-anchor",'start');
        
        // Accounts for the wraping of features
        if (name_string.length >= 20){
            text_shift += 25
        }
        else {text_shift += 15}

    }
    
    svg = svg.append("g")
            .attr("transform","translate(" + (text_space+text_feat+5) + ",0)")
    
      
    var good_row_count = 0,
        bad_row_count = 0;
    
    if (goodData.length == 0){y2_shift = 0;}
    else {y2_shift = 2*(sq_height + y_sep)+5;}


    // -- select border --
    svg.append('g').append("rect")
            .attr("class", "good-section-"+idx.toString())
            .attr('x',-5)
            .attr('y',-5)
            .attr("height",height/2+5)
            .attr("width",width-35)
            .attr("fill","none")
            .attr("stroke-opacity",0.8)
            .attr("stroke-width",0)
            .attr("stroke","#808080");


    svg.append('g').append("rect")
            .attr('x',-5)
            .attr("class", "bad-section-"+idx.toString())
            .attr('y',y2_shift-5)
            .attr("height",height/2+5)
            .attr("width",width-35)
            .attr("fill","none")
            .attr("stroke-opacity",0.8)
            .attr("stroke-width",0)
            .attr("stroke","#808080");
    
    var row_cap = 2;
    var drawn_idx = 0;
    for (indx = 0; indx < goodData.length; ++indx){        
        var single_square = goodData[indx];

        if (good_row_count == horizontal_limit) {
            row_cap -= 1
            good_row_count = 0;
            x1_shift = 0;
            y1_shift += (sq_height + y_sep);}

        if (row_cap == 0) {break;}


        var shifted_svg = svg.append('g')
                .attr("transform","translate(" + x1_shift + ',' + y1_shift +')')
                .attr("class", "mini-square-good-"+drawn_idx.toString());
            
            // --- FOR HOVERING ---
            shifted_svg.append("rect")
                .attr("class","smallsquare-"+single_square.id)
                .attr('x',0)
                .attr('y',0)
                .attr("height",sq_height)
                .attr("width",sq_width)
                .attr("fill-opacity",single_square.per*2-1)
                .attr("fill",good_col)
                .attr("stroke-width",0)
                .attr("stroke","black");
            
            var percent_string = Math.round(single_square.per*100).toString();
            
            shifted_svg.append('g').append("text")
                .text(percent_string)
                .attr("x",sq_width/2)
                .attr("y",sq_height/2+3)
                .attr("font-family", 'sans-serif')
                .attr("font-size", '9px')
                .attr("fill","white")
                .attr("text-anchor",'middle');
            
            x1_shift += sq_width + x_sep;
            good_row_count += 1;
            drawn_idx += 1;
        }
        
    
    var row_cap = 2;
    drawn_idx = 0;
    for (indx = 0; indx < badData.length; ++indx){
        
        var single_square = badData[indx];

        if (bad_row_count == horizontal_limit) {
            row_cap -= 1
            bad_row_count = 0;
            y2_shift += (sq_height + y_sep);
            x2_shift = 0;}

        if (row_cap == 0) {break;}

        var shifted_svg = svg.append('g')
                .attr("transform","translate(" + x2_shift + ',' + y2_shift +')')
                .attr("class", "mini-square-bad-"+drawn_idx.toString());  

        // --- FOR HOVERING ---
        shifted_svg.append('g').append("rect")
            .attr("class","smallsquare-"+single_square.id)
            .attr('x',0)
            .attr('y',0)
            .attr("height",sq_height)
            .attr("width",sq_width)
            .attr("fill-opacity",((single_square.per*-2)+1))
            .attr("stroke-width",0)
            .attr("stroke","black")
            .attr("fill",bad_col);

        var percent_string = Math.round(single_square.per*100).toString();

        shifted_svg.append('g').append("text")
            .text(percent_string)
            .attr("x",sq_width/2)
            .attr("y",sq_height/2+3)
            .attr("font-family", 'sans-serif')
            .attr("font-size", '9px')
            .attr("fill","white")
            .attr("text-anchor",'middle');


        x2_shift += sq_width + x_sep;
        bad_row_count += 1;
        drawn_idx += 1;
    }
}

function wrap(text, width) {
    text.each(function () {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            x = text.attr("x"),
            y = text.attr("y"),
            dy = 0, //parseFloat(text.attr("dy")),
            tspan = text.text(null)
                        .append("tspan")
                        .attr("x", x)
                        .attr("y", y)
                        .attr("dy", dy + "em");
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan")
                            .attr("x", x)
                            .attr("y", y)
                            .attr("dy", ++lineNumber * lineHeight + dy + "em")
                            .text(word);
            }
        }
    });
}
