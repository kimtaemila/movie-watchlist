const title = document.querySelector('input[name=title]')
const slug = document.querySelector('input[name=slug]')
const releaseDate = document.querySelector('input[name=releasedate]')

const slugify = (title, releaseDate) => {
    rFormat = releaseDate.replace(/[0-9]+\/[0-9]+\/(?=[0-9]{4})/g, '')
    tFormat = title.toString().toLowerCase().trim()
        .replace(/&/g, '-and-')
        .replace(/[\s\W-]+/g, '-')

    slugged = rFormat + '-' + tFormat
    return slugged
};

title.addEventListener('keyup', (e) => {
    slug.setAttribute('value', slugify(title.value, releaseDate.value))
});

releaseDate.addEventListener('input', (e) => {
    slug.setAttribute('value', slugify(title.value, releaseDate.value))
});
