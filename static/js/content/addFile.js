layui.use(["form","jquery","layedit","upload"],function(){
    var form = layui.form;
    var $ = layui.jquery;
    var layedit = layui.layedit;
    var upload = layui.upload;



    layedit.set({
        uploadImage: {
            url: '/content/uploadFile' //接口url
            ,type: 'POST' //默认post
        }
    });
    //建立编辑器
    var editIndex = layedit.build('editor');


    form.on("submit(save)",function(data){
        let params = data.field;
        let fileType = params.fileType;
        let imageName = params.imageName;
        if(fileType==="1"){
            var des = layedit.getContent(editIndex);
        }else if(fileType==="2"){
            var des = $("#upload img").attr("src");
        }else{
            var des = "";
        }
        let jsonData = {
            "parentId": params.parentId,
            "fileName": params.fileName,
            "fileType": fileType,
            "des": des,
            "imageName":imageName
        };
        $.ajax({
            type: "POST",
            url: "/content/addFile",
            data: jsonData,
            success: function(res){
                if(res.code===0){
                    layer.alert(res.msg, {icon: 6}, function () {
                        let index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                        parent.layer.close(index); //再执行关闭
                    });
                } else{
                    layer.alert(res.msg, {icon: 5});
                }
            },
            error:function(){
                layer.alert('操作失败，网络故障!', {icon: 5});
            }
        })
    });

    form.on("select(fileType)",function (data) {
        let fileType = data.value;
        let upload = $("#upload");
        let editor = $("#editor");
        let fileName = $("#fileName");
        if(fileType==="1"){
            upload.addClass("layui-hide");
            editor.parents(["div"]).removeClass("layui-hide");
        }else if(fileType==="2"){
            editor.parent().parent().addClass("layui-hide");
            fileName.removeAttr("lay-verify");
            fileName.parent().parent().addClass("layui-hide");
            upload.removeClass("layui-hide");
        }else{
            editor.parent().parent().addClass("layui-hide");
            upload.addClass("layui-hide");
        }
    });

    upload.render({
        elem: "#upload button"
        ,url: "/content/uploadFile"
        ,done: function(res){
            console.log(res);
            let html = '<img src="'+res.data.src+'" ><input type="hidden" name="imageName" value="'+res.data.title+'">';
            $("#upload").append(html)
        }
    })



});