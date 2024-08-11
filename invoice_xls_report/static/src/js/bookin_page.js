odoo.define('invoice_xls_report.bookin_page', function(require) {
    "use strict";
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;
    var ajax = require('web.ajax');
    require('web.dom_ready');
    var rpc = require('web.rpc');
    var p_id = 0;
    var p_product = 0;
    var p_cost = 0;
    var p_def = 0;
    var del = 0;
    var m2oid = 0
    var trclass = 0
    var session = require('web.session');
    var booking =  session.user_has_group('invoice_xls_report.group_web_url');
    var tag = document.querySelector("[href='/booking']")
    var path = document.location.pathname
    if (path=='/booking')
    {
        var img = $('#top_menu_container').find('img').attr('src', 'invoice_xls_report/static/img/booking-1.png');
        var connect = '<h5 class="mb-3">Connect with us</h5><ul class="list-unstyled"><li><i class="fa fa-comment fa-fw mr-2"/><span><a href="/contactus">Contact us</a></span></li><li><i class="fa fa-envelope fa-fw mr-2"/><span>Orders:  <a href="mailto:buyit@noxcuse4no.com">buyit@noxcuse4no.com</a></span></li><li><i class="fa fa-envelope fa-fw mr-2"/><span>Support:  <a href="mailto:helpit@noxcuse4no.com">helpit@noxcuse4no.com</a></span></li><li><i class="fa fa-envelope fa-fw mr-2"/><span>Suggestion:  <a href="mailto:improveit@noxcuse4no.com">improveit@noxcuse4no.com</a></span></li><li><i class="fa fa-skype fa-fw mr-2"/><span>Skype:  live:terry_236</a></span></li><li><i class="fa fa-phone fa-fw mr-2"/><span class="o_force_ltr"><a href="tel:+1 (650) 555-0111">+405-227-9046</a></span></li></ul><div class="s_share text-left" data-snippet="s_share" data-name="Social Media"><h5 class="s_share_title d-none">Follow us</h5><a href="/website/social/facebook" class="s_share_facebook" target="_blank"><i class="fa fa-facebook rounded-circle shadow-sm"/></a><a href="/website/social/twitter" class="s_share_twitter" target="_blank"><i class="fa fa-twitter rounded-circle shadow-sm"/></a><a href="/website/social/linkedin" class="s_share_linkedin" target="_blank"><i class="fa fa-linkedin rounded-circle shadow-sm"/></a><a href="/" class="text-800 float-right"><i class="fa fa-home rounded-circle shadow-sm"/></a></div>'
        $("#connect").html(connect)
    }

    if (session.user_id)
    {
        ajax.jsonRpc("/check/group", 'call', {}).then(function(group){
            if (group == 'Y')
            {
                tag.style.display = "block";
            }
            else
            {
                tag.style.display = "none";   
            }
        });

    }
    else if(!session.user_id)
    {
        tag.style.display = "block";
    }
    $('#product').on('click', function(){
        p_id++;
        p_product++;
        p_cost++;
        p_def++;
        del++
        m2oid ++
        trclass ++
        var m2o;
        var selction = '';
        ajax.jsonRpc("/fetch/products", 'call', {'product': 'product'}).then(function(product){
            var i;
            selction += '<select id="'+m2oid+'" name="m20" class="form-control m2o" placeholder="Select Product">';
            for ( i = 0; i < product.length; ++i) {
                    selction += "<option value=" + product[i].id + ">" + product[i].name + "</option>";
            }
            selction += '</select>';
            var html = '<tr id="tr-tag" class="'+trclass+'"><td style="width: 200px;">'+selction+'</td><td style="width: 200px;display:none;"><input type="text" class="form-control s_website_form_input" name="A'+p_id+'" placeholder="" id="A'+p_id+'"/></td><td style="width: 200px;"><input type="text" class="form-control s_website_form_input" id="B'+p_product+'" name="B'+p_product+'" placeholder=""/></td><td style="width: 200px;display:none;"><input type="text" class="form-control s_website_form_input" name="C'+p_def+'" id="C'+p_def+'" placeholder=""/></td><td style="width: 200px"><input type="text" class="form-control s_website_form_input cost" name="D'+p_cost+'" id="D'+p_cost+'" placeholder=""/></td><td style="width: 50px"><button class="removeRegular btn btn-danger" name="del" id="'+del+'">Delete</button></td></tr>'
            $('#tbody').append(html)
        });
    });
    $('#myTable').on('click', '.m2o', function(){
        // $(this).children("option:selected").val()
        var rows = $('#mytable tbody tr.selected');
        var ids=[];
        var product_id = $(this).attr('id')
        var classname = $(this). closest('tr').attr('class');
        $('.'+classname+' input[type="text"]').each(function(){
            ids.push($(this).attr('id'))
            // con/**/sole.log('----ddd---------' , $(this).attr('id'))
        })
        ajax.jsonRpc("/fetch/def-cost", 'call', {'product_id': $('#'+product_id).val()}).then(function(data){
            document.getElementById(ids[0]).value=data['id'];
            document.getElementById(ids[1]).value=data.name;
            document.getElementById(ids[2]).value=data['def'];
            document.getElementById(ids[3]).value=data['cost'];
            
        });

    });
    $("table tr").on('click', '#myTable tr', function(e){
        alert('Clicked row '+ ($(this).index()+1) );
    });
    $('#remove_row').on('click', function(){
        $('tr:last-child').remove();
    });
    $("#myTable").on('click', '.removeRegular', function(){
        $(this).parent().parent().remove();
    });
    $('#send').on('click', function(){
        var row = $("#myTable tr").length;
        document.getElementById('row').value=row;

    });

}); 

