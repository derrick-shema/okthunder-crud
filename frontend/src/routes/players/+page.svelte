<script lang="ts">
	import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    type Player = {
        id:number;
        first_name: string;
        last_name: string;
        position: string;
        height: string;
        image_url: string;
    }
    let players: Player[] = [];
    let loading = true;

    onMount(async () => {
        const res = await fetch('http://localhost:8000/api/players');
        players = await res.json();
        loading = false;
    });

    function goToAddPlayer() {
        // Replace with your add player route
        goto('/players/new');
    }
    function goToPlayer(id: number) {
        window.location.href = `/players/${id}`;
    }
</script>

<!-- ...existing script... -->

<section class="max-w-5xl mx-auto px-4 py-8 mr-4">
    <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-blue-700">Players</h1>
        <button
            class="bg-blue-700 text-white px-5 py-2 rounded hover:bg-blue-800 transition"
            on:click={goToAddPlayer}
        >
            + Add Player
        </button>
    </div>

    {#if loading}
        <p class="text-center text-gray-500">Loading players...</p>
    {:else if players.length === 0}
        <p class="text-center text-gray-500">No players found.</p>
    {:else}
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
            {#each players as player (player.id)}
                <button
                    type="button"
                    class="bg-white rounded shadow hover:shadow-lg transition cursor-pointer flex flex-col items-center p-6 focus:outline-none"
                    on:click={() => goToPlayer(player.id)}
                    aria-label={`View details for ${player.first_name} ${player.last_name}`}
                >
                    <img
                        src={`http://localhost:8000${player.image_url}`}
                        alt={player.first_name + ' ' + player.last_name}
                        class="w-32 h-32 object-cover rounded-full mb-4 border-2 border-blue-200"
                    />
                    <h2 class="text-xl font-semibold text-blue-700 mb-1">
                        {player.first_name} {player.last_name}
                    </h2>
                    <p class="text-gray-600 mb-1">{player.position}</p>
                    <p class="text-gray-500 text-sm">{player.height}</p>
                </button>
            {/each}
        </div>
    {/if}
</section>