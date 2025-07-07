<script lang="ts">
    import { goto } from '$app/navigation';

    let first_name = '';
    let last_name = '';
    let position = '';
    let height = '';
    let image: File | null = null;
    let loading = false;
    let error = '';

    async function handleSubmit(e: Event) {
        e.preventDefault();
        error = '';
        loading = true;

        const formData = new FormData();
        formData.append('first_name', first_name);
        formData.append('last_name', last_name);
        formData.append('position', position);
        formData.append('height', height);
        if (image) formData.append('image', image);

        const res = await fetch('http://localhost:8000/api/players', {
            method: 'POST',
            body: formData
        });

        loading = false;

        if (res.ok) {
            goto('/players');
        } else {
            const data = await res.json();
            error = data.detail || 'Failed to create player.';
        }
    }
</script>

<section class="max-w-xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-blue-700 mb-6">Add New Player</h1>
    <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
        <div>
            <label class="block mb-1 font-semibold" for="first_name">First Name</label>
            <input id="first_name" type="text" bind:value={first_name} required class="w-full border rounded px-3 py-2" />
        </div>
        <div>
            <label class="block mb-1 font-semibold" for="last_name">Last Name</label>
            <input id="last_name" type="text" bind:value={last_name} required class="w-full border rounded px-3 py-2" />
        </div>
        <div>
            <label class="block mb-1 font-semibold" for="position">Position</label>
            <input id="position" type="text" bind:value={position} required class="w-full border rounded px-3 py-2" />
        </div>
        <div>
            <label class="block mb-1 font-semibold" for="height">Height</label>
            <input id="height" type="text" bind:value={height} required class="w-full border rounded px-3 py-2" />
        </div>
        <div>
            <label class="block mb-1 font-semibold" for="image">Player Image</label>
            <input id="image" type="file" accept="image/*" on:change={e => image = (e.target as HTMLInputElement).files?.[0] ?? null} required class="w-full" />
        </div>
        {#if error}
            <p class="text-red-600">{error}</p>
        {/if}
        <button type="submit" class="bg-blue-700 text-white px-6 py-2 rounded hover:bg-blue-800 transition" disabled={loading}>
            {loading ? 'Adding...' : 'Add Player'}
        </button>
    </form>
</section>