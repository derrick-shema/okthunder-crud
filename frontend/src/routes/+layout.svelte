<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>
<body class="ml-8">
	<header class="flex items-center justify-between px-8 py-4">
		<div class="flex items-center gap-4">
			<img src="/okthunderlogo.png" alt="OKC Thunder Logo" width="100px" class="object-contain">
			<span class="text-2xl font-bold">OKCThunder</span>
		</div>
		<nav class="flex gap-6">
			<a href="/" class="hover:underline">Home</a>
			<a href="/players" class="hover:underline">Players</a>
		</nav>
	</header>
</body>

{@render children()}

