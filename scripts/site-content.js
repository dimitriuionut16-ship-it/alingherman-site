window.loadSiteContent = function(contentUrl) {
    fetch(contentUrl).then(function(response) {
        if (!response.ok) throw new Error('Cannot load site content: ' + response.status);
        return response.json();
    }).then(function(data) {
        Object.keys(data).forEach(function(key) {
            var el = document.querySelector('[data-content-key="' + key + '"]');
            if (el) {
                el.innerHTML = data[key];
            }
        });
    }).catch(function(err) {
        console.warn(err);
    });
};