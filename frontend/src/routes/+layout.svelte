<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>
<body class="ml-8">
	<header class="flex">
		<div class="flex ">
			<img src="/okthunderlogo.png" alt="OKC Thunder Logo" width="100px">
			<span>OKCThunder</span>
		</div>
	</header>
</body>


{@render children()}
