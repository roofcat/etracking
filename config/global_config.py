# -*- coding: utf-8 -*-
#!/usr/bin/env python


REPORT_EXPORT_URL = "https://azurian-rastreo.appspot.com/storage/report/{url_safe}/"
REPORT_SUBJECT_MAIL = "Reporte Generado por Azurian Tracking"
REPORT_HTML_MAIL = """
<meta charset="UTF-8">
<p>
Estimado/a {user_name}: <br> 
Azurian Tracking te ha enviado un reporte adjunto en excel que solicitaste. <br>
</p>
<footer>
<b>Azurian Tracking</b>
</footer>
<br>
"""