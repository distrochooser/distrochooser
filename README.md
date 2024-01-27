## distrochooser


<img src="https://distrochooser.de/static/logo.min.svg" width="50%" >

[![](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/vuejs/awesome-vue)

This repository contains the code of [distrochooser.de](http://distrochooser.de). 

The Distrochooser is a service to help Linux beginners to orientate. The service is not an oracle and can not calculate 100% accurate results, but it helps to orientate.

## Building locally

1. Use a venv to add the requirements from `./code/`. 
2. Import the matrix using `python3 manage.py parse ../../doc/matrix/beta/matrix.ku --wipe`(the --wipe flag is optional)
3. To build js and styles, cd into design and execute `yarn run build-styles` and `yarn run build-js` (make sure a folder static is present in the projects root dir)
4. Run `python3 manage.py collectstatic` (you will have to adapt the `settings.py` to point to the static folder before)
5. Run `python3 manage.py runserver`
6. Open localhost:8000


## License

See LICENSE


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/christianmalek"><img src="https://avatars2.githubusercontent.com/u/2873986?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Christian Malek</b></sub></a><br /><a href="#design-christianmalek" title="Design">🎨</a> <a href="https://github.com/distrochooser/distrochooser/commits?author=christianmalek" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/PositiveKoodoo"><img src="https://avatars3.githubusercontent.com/u/48484929?v=4?s=100" width="100px;" alt=""/><br /><sub><b>PositiveKoodoo</b></sub></a><br /><a href="#translation-PositiveKoodoo" title="Translation">🌍</a></td>
    <td align="center"><a href="https://maddosaurus.github.io"><img src="https://avatars1.githubusercontent.com/u/8026915?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Matthias</b></sub></a><br /><a href="#translation-Maddosaurus" title="Translation">🌍</a></td>
    <td align="center"><a href="https://zmoazeni.github.io/gitspective/#/timeline/waldyrious"><img src="https://avatars2.githubusercontent.com/u/478237?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Waldir Pimenta</b></sub></a><br /><a href="#translation-waldyrious" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/jollypuppet"><img src="https://avatars0.githubusercontent.com/u/55812399?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Andrea</b></sub></a><br /><a href="#translation-jollypuppet" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/z1r0-"><img src="https://avatars2.githubusercontent.com/u/6104256?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Alex Sa</b></sub></a><br /><a href="#question-z1r0-" title="Answering Questions">💬</a> <a href="https://github.com/distrochooser/distrochooser/commits?author=z1r0-" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/xingjiapeng"><img src="https://avatars0.githubusercontent.com/u/47733616?v=4?s=100" width="100px;" alt=""/><br /><sub><b>xingjiapeng</b></sub></a><br /><a href="#translation-xingjiapeng" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://koji00.me/"><img src="https://avatars3.githubusercontent.com/u/43900679?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Minh Ngo</b></sub></a><br /><a href="#translation-streetsamurai00mi" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/igwigg"><img src="https://avatars2.githubusercontent.com/u/5790079?v=4?s=100" width="100px;" alt=""/><br /><sub><b>igwigg</b></sub></a><br /><a href="#translation-igwigg" title="Translation">🌍</a></td>
    <td align="center"><a href="https://fosstodon.org/web/accounts/278904"><img src="https://avatars.githubusercontent.com/u/60455393?v=4?s=100" width="100px;" alt=""/><br /><sub><b>explorer422</b></sub></a><br /><a href="#translation-explorer422" title="Translation">🌍</a></td>
    <td align="center"><a href="https://nathanbonnemains.squill.fr/"><img src="https://avatars.githubusercontent.com/u/45366162?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nathan Bonnemains</b></sub></a><br /><a href="#translation-NathanBnm" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/binarynoise"><img src="https://avatars.githubusercontent.com/u/50302352?v=4?s=100" width="100px;" alt=""/><br /><sub><b>binarynoise</b></sub></a><br /><a href="#translation-binarynoise" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/jalovisko"><img src="https://avatars.githubusercontent.com/u/22379984?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nikita Letov</b></sub></a><br /><a href="#translation-jalovisko" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/henrydenhengst"><img src="https://avatars.githubusercontent.com/u/8768292?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Henry den Hengst</b></sub></a><br /><a href="#translation-henrydenhengst" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/omeritzics"><img src="https://avatars.githubusercontent.com/u/66558205?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Omer I.S.</b></sub></a><br /><a href="#question-omeritzics" title="Answering Questions">💬</a> <a href="#translation-omeritzics" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/EinPinsel"><img src="https://avatars.githubusercontent.com/u/12642546?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Stefan H.</b></sub></a><br /><a href="#infra-EinPinsel" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://github.com/ciacon"><img src="https://avatars.githubusercontent.com/u/49395?v=4?s=100" width="100px;" alt=""/><br /><sub><b>ciacon</b></sub></a><br /><a href="#translation-ciacon" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/Schuermi7"><img src="https://avatars.githubusercontent.com/u/12413787?v=4?s=100" width="100px;" alt=""/><br /><sub><b>schuermi7</b></sub></a><br /><a href="https://github.com/distrochooser/distrochooser/commits?author=Schuermi7" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/pabloab"><img src="https://avatars.githubusercontent.com/u/657836?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Pablo</b></sub></a><br /><a href="#translation-pabloab" title="Translation">🌍</a></td>
    <td align="center"><a href="https://gitlab.com/AstolfoKawaii"><img src="https://avatars.githubusercontent.com/u/42834568?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Astolfo</b></sub></a><br /><a href="#translation-AstolfoKawaii" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/heidiwenger"><img src="https://avatars.githubusercontent.com/u/82445727?v=4?s=100" width="100px;" alt=""/><br /><sub><b>heidiwenger</b></sub></a><br /><a href="#translation-heidiwenger" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/kajuboii"><img src="https://avatars.githubusercontent.com/u/73589113?v=4?s=100" width="100px;" alt=""/><br /><sub><b>OMER FARUK KUCUKONDER</b></sub></a><br /><a href="#translation-kajuboii" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/nkot56297"><img src="https://avatars.githubusercontent.com/u/95204402?v=4?s=100" width="100px;" alt=""/><br /><sub><b>nkot56297</b></sub></a><br /><a href="#translation-nkot56297" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/EmirLogas"><img src="https://avatars.githubusercontent.com/u/76751818?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Emir</b></sub></a><br /><a href="#translation-EmirLogas" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/mothsART"><img src="https://avatars.githubusercontent.com/u/10601196?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jérémie Ferry</b></sub></a><br /><a href="#translation-mothsART" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/msmafra"><img src="https://avatars.githubusercontent.com/u/1005457?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Marcelo dos Santos Mafra</b></sub></a><br /><a href="#translation-msmafra" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/OkayPJ"><img src="https://avatars.githubusercontent.com/u/47733616?v=4?s=100" width="100px;" alt=""/><br /><sub><b>OkayPJ</b></sub></a><br /><a href="#translation-OkayPJ" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/cat0x1f"><img src="https://avatars.githubusercontent.com/u/72690879?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sen_Yue</b></sub></a><br /><a href="#translation-cat0x1f" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/fbp110"><img src="https://avatars.githubusercontent.com/u/96155179?v=4?s=100" width="100px;" alt=""/><br /><sub><b>fbp110</b></sub></a><br /><a href="#translation-fbp110" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/zephyroths"><img src="https://avatars.githubusercontent.com/u/19946761?v=4?s=100" width="100px;" alt=""/><br /><sub><b>zephyroths</b></sub></a><br /><a href="#translation-zephyroths" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/FKAgony"><img src="https://avatars.githubusercontent.com/u/117533462?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Agony</b></sub></a><br /><a href="#translation-FKAgony" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/WX4300"><img src="https://avatars.githubusercontent.com/u/113265063?v=4?s=100" width="100px;" alt=""/><br /><sub><b>WX4300</b></sub></a><br /><a href="#translation-WX4300" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/Agayev033"><img src="https://avatars.githubusercontent.com/u/30019351?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Agayev033</b></sub></a><br /><a href="#translation-Agayev033" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/codehangen"><img src="https://avatars.githubusercontent.com/u/111701513?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Code Hangen</b></sub></a><br /><a href="#a11y-codehangen" title="Accessibility">️️️️♿️</a> <a href="#question-codehangen" title="Answering Questions">💬</a> <a href="#ideas-codehangen" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!
