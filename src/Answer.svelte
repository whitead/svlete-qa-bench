<script>
    import { fade } from 'svelte/transition';
    export let question = "";
    export let answer = "";
    export let date = "";
    export let model = "";
    export let sources = [];
  
    let showSources = false;

    function toggleSources() {
    showSources = !showSources;
    }

  
    function findCitations(input) {
        const bracketPattern = /\[(\d+(-\d+)?(?:,\d+(-\d+)?)*)\]/g;
        const wordPattern = /\(([^\d\s()]+(?:\d{4})(?:,\s?[^\d\s()]+(?:\d{4}))*)\)/g;
        const output = [];

        let bracketMatch;
        while ((bracketMatch = bracketPattern.exec(input)) !== null) {
            const range = bracketMatch[1].split(',');
            range.forEach(item => {
            if (item.includes('-')) {
                const [start, end] = item.split('-').map(Number);
                for (let i = start; i <= end; i++) {
                output.push({ start: bracketMatch.index, end: bracketPattern.lastIndex, key: i.toString() });
                }
            } else {
                output.push({ start: bracketMatch.index, end: bracketPattern.lastIndex, key: item });
            }
            });
        }

        let wordMatch;
        while ((wordMatch = wordPattern.exec(input)) !== null) {
            const words = wordMatch[1].split(/,\s?/);
            words.forEach(word => {
            output.push({ start: wordMatch.index, end: wordPattern.lastIndex, key: word });
            });
        }

        return output;
    }

    const citations = findCitations(answer);

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
        {#each citations as citation, i}
          {answer.slice(i === 0 ? 0 : citations[i - 1].end, citation.start)}
          <sup>
            <a
              tabindex="0"
              class="citation"
              on:click={toggleSources}
            >{answer.slice(citation.start, citation.end)}</a>
          </sup>
          {#if i === (citations.length - 1)}
            {answer.slice(citation.end)}
          {/if}
        {/each}
      </p>
    {#if showSources}
    <div  transition:fade>
      {#each sources as reference}
        <p class="reference">[{reference.key}] {reference.text}</p>
      {/each}
    </div>
    {/if}
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
        color: #EE3333;
    }

    .answer {
        margin-bottom: 20px;
    }

    .details {
        font-size: 0.9em;
        
    }

    .citation {
        text-decoration: none;
        color: #3322AA;
        cursor: pointer;
    }

    .reference {
        margin-bottom: 8px;
    }
</style>
