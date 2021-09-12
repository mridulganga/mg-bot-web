<script>
	import ChatMessage from './ChatMessage.svelte';
	import Fa from 'svelte-fa';
	import { faUsers, faCompressArrowsAlt, faComments, faEnvelope } from '@fortawesome/free-solid-svg-icons';
  import marked from 'marked'

  const client = mqtt.connect('wss://hmq.mridulganga.dev:1888/ws',{
    retain: true
  });

  let autoScroll = true

  $: connected = client.connected

  client.on('connect', function () {
    connected=client.connected
  client.subscribe('mgsimplechat', function (err) {
    console.log("subscribed to mgsimplechat")
    if (!err) {
      // client.publish('mgsimplechat', 'Hello mqtt')
    }
  })
})


client.on('reconnect', (error) => {
    console.log('reconnecting:', error)
})

client.on('error', (error) => {
    console.log('Connection failed:', error)
})

client.on('message', function (topic, message) {
  // message is Buffer
  var msg = JSON.parse(message)
  messages = [...messages,msg]
  if (autoScroll){
    setTimeout(function(){
      document.querySelector('.container').scrollIntoView(false);
    },50)
  }
})

	let nameMe='mridul';
  let messageText = "";

  const onKeyPress = e => {
    if (e.charCode === 13) sendMessage();
  };

	function sendMessage(){

    if (client.connected){
      client.publish('mgsimplechat', JSON.stringify(
        {
          name: nameMe,
          message: messageText,
          timestamp: Date.now()
        }
      ))
    }
		messageText=""
    if (autoScroll){
      document.querySelector('.container').scrollIntoView(false);
    }
	}
	
	let messages = [
  {
    "name": "416",
    "message": "abc",
    "timestamp": 1587139022488.826
  },
  {
    "name": "417",
    "message": "test",
    "timestamp": 1587139034294.678
  },
  {
    "name": "mridul",
    "message": "a",
    "timestamp": 1587139047495.052
  },
  {
    "name": "419",
    "message": "testset",
		"hasImage": true,
		"image": "https://media.istockphoto.com/photos/grey-stripped-mixedbreed-cat-sitting-isolated-on-white-picture-id1217828258?b=1&k=20&m=1217828258&s=170667a&w=0&h=jVuou3wnJ1x7eLf0iWS53BvA5ZOyROTBfiTM3tPhD4g=",
    "timestamp": 1587139312376.663
  },
  {
    "name": "420",
    "message": "a cat gif",
		"image":"https://media1.giphy.com/media/ICOgUNjpvO0PC/giphy.gif",
		"hasImage": true,
    "timestamp": 1587139349155.217
  },
  {
    "name": "mridul",
    "message": "t",
    "timestamp": 1587577393781.811
  },
  {
    "name": "427",
    "message": "aaa",
    "timestamp": 1587577411018.97
  },
  {
    "name": "431",
    "message": "a",
    "timestamp": 1587652540004.281
  },
  {
    "name": "mridul",
    "message": "u",
    "timestamp": 1587686520069.1272
  },
  {
    "name": "433",
    "message": "a",
    "timestamp": 1587782491376.533
  }
]



</script>



<style>
  html,body{
    height: 100%;
    width: 100%;
  }
	.direct-chat .card-body {
		overflow-x: hidden;
		padding: 0;
		position: relative;
	}

	.direct-chat-messages {
		-webkit-transform: translate(0, 0);
		transform: translate(0, 0);
		height: 100%;
    width: 100%;
		overflow: auto;
		padding: 10px;
		transition: -webkit-transform .5s ease-in-out;
		transition: transform .5s ease-in-out;
		transition: transform .5s ease-in-out, -webkit-transform .5s ease-in-out;
    margin-bottom: 200px;
	}
  .card-footer{
    background: white;
  }
</style>

<svelte:head>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
</svelte:head>


<div class="container">
  <div class="row">
    <div class="col-sm-3">
      
    </div>
    <div class="col-sm-6">
      <div class="card card-danger direct-chat direct-chat-danger">
        <div class="card-header">
            <div class="card-tools d-flex">
                <span class="contacts-name">{connected?"Welcome to chat":"connecting"}</span>
              <div class="mr-auto"></div>
                <input type="text" placeholder="Type Name here" class="float-right" bind:value={nameMe}>
            </div>
        </div>
        <div class="card-body">
            <div class="direct-chat-messages">
                {#each messages as message}
                    <ChatMessage
                        name = {message.name}
                        message={marked(message.message)}
                        timestamp={message.timestamp}
                        isMe={message.name==nameMe}
                        image={message.image}
                        hasImage={message.hasImage}
                        />
                {/each}
            </div>
        </div>
    </div>
    <div class="card-footer fixed-bottom">
      <div class="row">
        <div class="col-sm-3">
          <input type="checkbox" bind:checked={autoScroll}> Auto Scroll
        </div>
        <div class="col-sm-6">
          <div class="input-group">
            <input type="text" placeholder="Type Message ..." class="form-control" bind:value={messageText} on:keypress={onKeyPress}>
            <span class="input-group-append">
                <button type="button" class="btn btn-primary" on:enter on:click={sendMessage}>Send</button>
            </span>
        </div>
      </div>
      </div>
        
    </div>
    </div>
  </div>
</div>

