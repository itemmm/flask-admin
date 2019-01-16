layui.use(["form","jquery"],function(){
    var form = layui.form;
    var $ = layui.jquery;

    form.on("submit(login)",function(data){
       let params = data.field;
       let loginName = params.loginName;
       let passWord = hex_md5(params.passWord);
       $.ajax({
           type: "POST",
           url: "/business/login",
           data: {"loginName":loginName,"passWord":passWord},
           success:function(res){
               if(res.code===0){
                   window.location.href='/business/index';
               }else{
                   layer.alert(res.msg, {icon: 5});
               }
           },
           error:function(){
               layer.alert('操作失败，网络故障!', {icon: 5});
           }
       })
    });

});