<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { get } from 'svelte/store';
    import { goto } from '$app/navigation';

    let player: {
        id: number;
        first_name: string;
        last_name: string;
        position: string;
        height: string;
        image_url: string;
    } | null = null;
    let loading = true;
    let error = '';
    let deleting = false;

    onMount(async () => {
        const id = get(page).params.id;
        try {
            const res = await fetch(`http://localhost:8000/api/players/${id}`);
            if (!res.ok) throw new Error('Player not found');
            player = await res.json();
        } catch (e) {
            error = 'Could not load player.';
        }
        loading = false;
    });

    async function handleDelete() {
        if (!player) return;
        if (!confirm('Are you sure you want to delete this player?')) return;
        deleting = true;
        const res = await fetch(`http://localhost:8000/api/players/${player.id}`, {
            method: 'DELETE'
        });
        deleting = false;
        if (res.ok) {
            goto('/players');
        } else {
            error = 'Failed to delete player.';
        }
    }

    function handleUpdate() {
        if (player) {
            goto(`/players/${player.id}/edit`);
        }
    }
</script>

<section class="max-w-xl mx-auto px-4 py-10">
    {#if loading}
        <p class="text-center text-gray-500">Loading player...</p>
    {:else if error}
        <p class="text-center text-red-600">{error}</p>
    {:else if player}
        <div class="bg-white rounded shadow p-8 flex flex-col items-center">
            <img
                src={`http://localhost:8000${player.image_url}`}
                alt={player.first_name + ' ' + player.last_name}
                class="w-40 h-40 object-cover rounded-full mb-6 border-2 border-blue-200"
            />
            <h1 class="text-3xl font-bold text-blue-700 mb-2">
                {player.first_name} {player.last_name}
            </h1>
            <p class="text-lg text-gray-700 mb-1">
                <span class="font-semibold">Position:</span> {player.position}
            </p>
            <p class="text-lg text-gray-700 mb-1">
                <span class="font-semibold">Height:</span> {player.height}
            </p>
            <div class="flex gap-4 mt-6">
                <button
                    class="bg-blue-700 text-white px-5 py-2 rounded hover:bg-blue-800 transition"
                    on:click={handleUpdate}
                >
                    Update
                </button>
                <button
                    class="bg-red-600 text-white px-5 py-2 rounded hover:bg-red-700 transition disabled:opacity-50"
                    on:click={handleDelete}
                    disabled={deleting}
                >
                    {deleting ? 'Deleting...' : 'Delete'}
                </button>
            </div>
            <a href="/players" class="mt-6 text-blue-700 hover:underline">&larr; Back to Players</a>
        </div>
    {/if}
</section>