			var hostLink = "http://122.51.67.37:5000"
			//var hostLink = "http://127.0.0.1:5000"
		String.prototype.format=function()  
{  
  if(arguments.length==0) return this;  
  for(var s=this, i=0; i<arguments.length; i++)  
    s=s.replace(new RegExp("\\{"+i+"\\}","g"), arguments[i]);  
  return s;  
};
  function getElemeInnerHTML() {

    $.ajax({  
            type: "GET",   //提交的方法
            url:hostLink+"/wxBot1/eleme", //提交的地址
            //data:$('#form-eleme').serialize(),// 序列化表单值  
            async: false,  
            error: function(request) {  //失败的话
                 alert("Connection error");  
            },  
            success: function(ret) {  //成功	 
					var data = JSON.parse(ret)
					if(data.code == 200 && data.result != 'false'){
						var lists = data.result
						var strHtml = ""
						var dic = new Array();
						var strMubanTextarea = "<span class=\"input input--minoru\"><textarea  class=\"input__field input__field--minoru\" type=\"text\" id=\"input-eleme{0}\"  rows=\"5\" value=\"\" name=\"split-{1}\" /></textarea ><label class=\"input__label input__label--minoru\" for=\"input-13\"><span class=\"input__label-content input__label-content--minoru\">{2}</span></label></span><br>"
						var strMuban = "<span class=\"input input--minoru\"><input  class=\"input__field input__field--minoru\" type=\"text\" id=\"input-eleme{0}\"  value=\"{1}\" name=\"split-{2}\" /><label class=\"input__label input__label--minoru\" for=\"input-13\"><span class=\"input__label-content input__label-content--minoru\">{3}</span></label></span><br>"

					        for (var i = 0; i < lists.length; i++) {
								k = i+1
								if (lists[i].text.length>30)
								{
									var dakaObj = strMubanTextarea.format(k.toString(), k.toString(),lists[i].text_info);
									dic[ k.toString()] = lists[i].text;
								}else{
									var dakaObj = strMuban.format(k.toString(), lists[i].text, k.toString(),lists[i].text_info);
								}
								
								strHtml+=dakaObj;
								  }
						var d1 = document.getElementById('insEleme'); 
						d1.insertAdjacentHTML('afterend', strHtml);	
						//document.getElementById('input-eleme1').value="①饿了么拼手气红包监控（使用教程：https://url.cn/5oPZAea）";
							   for (var key in dic) {
									document.getElementById('input-eleme'+key).value=dic[key];
            }


				 }//就将返回的数据显示出来
                 //window.location.href="跳转页面"  
            }  
         });

    $.ajax({  
            type: "GET",   //提交的方法
            url:hostLink+"/wxBot1/daka", //提交的地址
            //data:$('#form-eleme').serialize(),// 序列化表单值  
            async: false,  
            error: function(request) {  //失败的话
                 alert("Connection error");  
            },  
            success: function(ret) {  //成功	 
					var data = JSON.parse(ret)
					if(data.code == 200 && data.result != 'false'){
						var lists = data.result
						var strHtml = ""
						var strMuban = "<span class=\"input input--minoru\"><input  class=\"input__field input__field--minoru\" type=\"text\" id=\"input-daka{0}\"  value=\"{1}\" name=\"text{2}\" /><label class=\"input__label input__label--minoru\" for=\"input-13\"><span class=\"input__label-content input__label-content--minoru\">时段{3}</span></label></span><br>"

					        for (var i = 0; i < lists.length; i++) {
								k = i+1
								var dakaObj = strMuban.format(k.toString(),lists[i], k.toString(),k.toString());
								strHtml+=dakaObj;
								  }
						var d1 = document.getElementById('insDaka'); 
						d1.insertAdjacentHTML('afterend', strHtml);					

				 }//就将返回的数据显示出来
                 //window.location.href="跳转页面"  
            }  
         });

              //发送异步请求

              //1.创建ajax引擎对象----所有操作都是由ajax引擎完成

									

       }
		
	getElemeInnerHTML();

  $("#but-eleme").click(function () {
    $.ajax({  
            type: "POST",   //提交的方法
            url:hostLink+"/wxBot1/eleme", //提交的地址
            data:$('#form-eleme').serialize()+"&token="+getQueryVariable("token"),// 序列化表单值  
            async: false,  
            error: function(request) {  //失败的话
                 alert("Connection error");  
            },  
            success: function(data) {  //成功
                 alert(JSON.parse(data).msg);  //就将返回的数据显示出来
            } 
			
         });
       }); 

	$("#but-daka").click(function () {
    $.ajax({  
            type: "POST",   //提交的方法
            url:hostLink+"/wxBot1/daka", //提交的地址
            data:$('#form-daka').serialize()+"&token="+getQueryVariable("token"),// 序列化表单值  
            async: false,  
            error: function(request) {  //失败的话
                 alert("Connection error");  
            },  
            success: function(data) {  //成功
                 alert(JSON.parse(data).msg);  //就将返回的数据显示出来
                 //window.location.href="跳转页面"  
            }  
         });
       }); 

	     $("#but-sign-state").click(function () {
    $.ajax({  
            type: "POST",   //提交的方法
            url:hostLink+"/wxBot1/updateSignState", //提交的地址
            data:$('#form-sign-state').serialize()+"&token="+getQueryVariable("token"),// 序列化表单值  
            async: false,  
            error: function(request) {  //失败的话
                 alert("Connection error");  
            },  
            success: function(data) {  //成功
                 alert(JSON.parse(data).msg);  //就将返回的数据显示出来
                 //window.location.href="跳转页面"  
            }  
         });
       }); 

	$("#but-daka-state").click(function () {
    $.ajax({  
            type: "POST",   //提交的方法
            url:hostLink+"/wxBot1/updateDakaState", //提交的地址
            data:$('#form-daka-state').serialize()+"&token="+getQueryVariable("token"),// 序列化表单值  
            async: false,  
            error: function(request) {  //失败的话
                 alert("Connection error");  
            },  
            success: function(data) {  //成功
                 alert(JSON.parse(data).msg);  //就将返回的数据显示出来
                 //window.location.href="跳转页面"  
            }  
         });
       }); 

		$("#but-upName").click(function () {
    $.ajax({  
            type: "POST",   //提交的方法
            url:hostLink+"/wxBot1/upHtmlName", //提交的地址
            data:{
				token:getQueryVariable("token")
				//"202cb962ac59075b964b07152d234b70"
					//getQueryVariable("token")
			},// 序列化表单值  
            async: false,  
            error: function(request) {  //失败的话
                 alert("Connection error");  
            },  
            success: function(data) {  //成功
                 alert(JSON.parse(data).msg);  //就将返回的数据显示出来
                 //window.location.href="跳转页面"  
            }  
         });
       }); 

//读取地址栏参数函数
	function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){
				   //alert(pair[1]);
				   return pair[1];
				   }
       }
       return(false);
}
//alert(hostLink+getQueryVariable("id"));
//getQueryVariable("id");