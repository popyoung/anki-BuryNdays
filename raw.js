function setup(options) {
    const store = options.auxData();
    const boolInput = document.getElementById("acrossDecks");
    const numberInput = document.getElementById("buryInterval");
  
    // update html when state changes
    store.subscribe((data) => {
      boolInput.checked = data["acrossDecks"];
      numberInput.value = data["buryInterval"];
  
      // and show current data for debugging
    //   document.getElementById("myDebug").innerText = JSON.stringify(
    //     data,
    //     null,
    //     4
    //   );
    });
  
    // update config when check state changes
    boolInput.addEventListener("change", (_) =>
      store.update((data) => {
        return { ...data, acrossDecks: boolInput.checked };
      })
    );
    numberInput.addEventListener("change", (_) => {
      let number = 0;
      try {
        number = parseInt(numberInput.value, 10);
      } catch (err) {}
  
      return store.update((data) => {
        return { ...data, buryInterval: number };
      });
    });
  }
  
  $deckOptions.then((options) => {
    options.addHtmlAddon(HTML_CONTENT, () => setup(options));
  });