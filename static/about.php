<div class="modal fade" id="myModal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 id="Title" class="ldcui modal-title">Modal title</h4>
      </div>
      <div class="modal-body">
        <p id="aboutText" class="ldcui"></p>
        <h3 id="installedDistros" class="ldcui">Aktuell einbezogene Distributionen</h3>
        <ul>
          <li v-for="distro in ldc.distributions">
            <a href="{{distro.Website}}">{{distro.Name}}</a>
          </li>
        </ul>
        <h3 id="stats" class="ldcui">Statistiken</h3>
        <p>Tests: {{ testCount }}</p>
        <p>Hits: {{ visitorCount }}</p>
        <h4 id="uses" class="ldcui">Distrochooser wird ermöglicht durch</h4>
        <ul>
          <li><a href="http://getbootstrap.com/">Bootstrap</a></li>
          <li><a href="https://bootswatch.com/lumen/">Bootswatch Theme Lumen</a></li>
          <li><a href="https://vuejs.org">vue.js</a></li>
          <li><a href="https://jquery.com/">jQuery</a></li>
          <li><a href="http://www.deviantart.com/art/Tondo-F-Icon-Set-OS-327759704">Tux Icon von P3T3B3</a></li>
          <li><a href="http://cmalek.de">Phis</a> (Design)</li>
          <li><a href="https://dribbble.com/shots/1211759-Free-195-Flat-Flags">Flat flag icons -  Muharrem Şenyıl</a></li>
          <li>Lenny (Manjaro Screenshots)</li>
          <li><a href="https://prrashi.github.io/rateYo/">rateYo</a></li>

        </ul>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->