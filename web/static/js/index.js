



function clickExample(){
  

  $.ajax({
    type: "POST",
    dataType:'json',
    url: "/ping",
    data: {
        ping:true
    },
    success: (data) =>{
      alert("Yay you Pinged")
      console.log(data)
    },
    fail: (error) =>{
        alert("Oh no you couldnt ping");
        console.log(error);
    }
  });
}