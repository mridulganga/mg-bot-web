<script>
	import Fa from 'svelte-fa';
	import { faCheck, faCheckDouble } from '@fortawesome/free-solid-svg-icons';
	
    export let isMe;
    export let name;
		export let message;
    export let timestamp;	
		export let hasImage = false;
		export let image;
	
</script>

<style>
.direct-chat-msg,
.direct-chat-text {
	display: block;
}
.direct-chat-msg {
	margin-bottom: 10px;
}
.direct-chat-msg:before,
.direct-chat-msg:after {
	content: " ";
	display: table;
}
.direct-chat-msg:after {
	clear: both;
}
.direct-chat-text {
	border-radius: 5px;
	position: relative;
	padding: 5px 10px;
	background: #bdc3c7;
	border: 1px solid #bdc3c7;
	margin: 2px 0 5px 50px;
	color: #444;
			margin-right: 50px;
}
.direct-chat-text:after,
.direct-chat-text:before {
	position: absolute;
	right: 100%;
	top: 15px;
	border: solid transparent;
	border-right-color: #d2d6de;
	content: ' ';
	height: 0;
	width: 0;
	pointer-events: none;
}
.direct-chat-text:after {
	border-width: 5px;
	margin-top: -5px;
}
.direct-chat-text:before {
	border-width: 6px;
	margin-top: -6px;
}
.right .direct-chat-text {
	margin-right: 50px;
	margin-left: 50px;
	background:#ecf0f1;
	border: 1px solid #ecf0f1;
}
.right .direct-chat-text:after,
.right .direct-chat-text:before {
	right: auto;
	left: 100%;
	border-right-color: transparent;
	border-left-color: #d2d6de;
}	
	.direct-chat-infos {
			font-size: .8rem;
		
	}
.direct-chat-name {
	margin-left: 50px;
	margin-right: 50px;
	font-weight: 600;
}
.direct-chat-timestamp {
	margin-left: 50px;
	margin-right: 50px;
	color: #999;

	margin-bottom: 0;
}
</style>

<div class="direct-chat-msg" class:right="{isMe}" class:left="{!isMe}">
    <div class="direct-chat-infos clearfix">
			
			   <span class="direct-chat-name" class:float-right="{isMe}" class:float-left="{!isMe}">{name}</span>
			
			
        <span class="direct-chat-timestamp" class:float-left="{isMe}" class:float-right="{!isMe}">
					{new Date(timestamp).toLocaleString([], {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute:'2-digit', hour12: false})}
				</span>
    </div>
    <div class="direct-chat-text">
			{#if hasImage}
				<img src={image} alt="" width="100%">
			{/if}
			<div class="d-flex">
				<span class="mr-auto">{@html message}</span>
		</div>
	</div>
</div>