$(document).ready(function() {
    $(":file").on("change", function() {
        document.querySelector(".images").innerHTML = '';
        document.querySelector(".show").innerHTML = '';
        image = this.files[0];
        reader = new FileReader();
        img = document.createElement("img");
        reader.readAsDataURL(image);
        reader.addEventListener("load", function() {
            img.src = reader.result;
            $(".images").append(img);
        }, false)
    });
    $(":submit").click(function(e) {
        file = document.querySelector("input[type=file]");
        if (file.value == "") {
            alert("champ vide");
            e.preventDefault();
        } else {
            setTimeout(()=>{

                $.ajax({
                    url: "static/detect.txt",
                    tryCount : 0,
                    retryLimit : 3,
                    success: function(result) {
                        line = result.split('}');
                        $(".show").html('');
                        for (var i = 0; i < line.length - 1; i++) {
                            line[i] = line[i].concat('}');
                            variable = JSON.parse(line[i]);
                            if (i == 0) {
                                maxPred = variable['precision'];
                            }
                            cls = document.createElement("h3");
                            cls.innerHTML = variable['prediction'];
                            prog = document.createElement("progress");
                            prog.max = 100;
                            prog.value = variable['precision'];
                            br = document.createElement("br");
                            $(".show").append(cls);
                            $(".show").append(prog);
                            $(".show").append(br);
                        }
                        if (maxPred >= 90) {
                            add = document.createElement("input");
                            add.type = "button";
                            add.value = "Ajouter";
                            add.id = "add";
                            add.style="display:block;margin-left:20px;position:relative;left:30px;";
                            $(".images").append(add);
                        }
                    },
                    error : function(xhr, textStatus, errorThrown ) {
                        if (textStatus == 'timeout') {
                            this.tryCount++;
                            if (this.tryCount <= this.retryLimit) {
                                $.ajax(this);
                                return;
                            }            
                            return;
                        }

                    }
                });
            },3000);
                
        }
    });
    $('.images').bind('DOMSubtreeModified', function(){
        $("#add").click(()=>{
            alert("merci !!!");
            location.href = "/add";
            $(this).children().last().remove();
        })
    });
});