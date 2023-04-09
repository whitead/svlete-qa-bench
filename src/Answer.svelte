<script>
    import { fade } from "svelte/transition";
    export let question = "";
    export let answer = "";
    export let date = "";
    export let model = "";
    export let sources = [];

    let showSources = false;

    function toggleSources() {
        showSources = !showSources;
    }

    
</script>

<main>
    <!-- <p class="question">{question}</p> -->
    <div class="details">
        <table>
            <tr>
                <td>model:</td>
                <td class="model">{model}</td>
            </tr>
            <tr>
                <td>date:</td>
                <td>{date}</td>
            </tr>
        </table>
        <p class="answer">
            {answer}
        </p>
        <button on:click={toggleSources}>
            {#if showSources}
                hide sources
            {:else}
                show sources
            {/if}
        </button>
        {#if showSources}
            <div transition:fade>
                {#each sources as reference}
                    <p class="reference">[{reference.key}] {reference.text}</p>
                {/each}
            </div>
        {/if}
    </div>
</main>

<style>
    main {
        background-color: antiquewhite;
        padding: 20px;
        max-width: 800px;
        margin: auto;
        border: 1px solid black;
    }

    td {
        padding-right: 5px;
    }
    .question {
        font-size: 1.5em;
    }

    .model {
        font-weight: bold;
        color: #ee3333;
    }

    .answer {
        margin-bottom: 20px;
    }

    .details {
        font-size: 0.9em;
    }

    .citation {
        text-decoration: none;
        color: #3322aa;
        cursor: pointer;
    }

    .reference {
        margin-bottom: 8px;
    }
</style>
