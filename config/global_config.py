# -*- coding: utf-8 -*-
#!/usr/bin/env python


REPORT_EXPORT_URL = "https://azurian-rastreo.appspot.com/storage/report/{url_safe}/"
REPORT_SUBJECT_MAIL = "Reporte Generado por Azurian Tracking"
REPORT_HTML_MAIL = """
<meta charset="UTF-8">
<p>
Estimado/a {user_name}: <br> 
Se ha generado el reporte en formato excel puedes acceder a el mediante el siguiente link: <br>
<a style="text-decoration:none;color:#3F51B5;" href="{report_link}" target="_blank">
Click para ir al documento</a> <br>
<b>NOTA:</b> Sólo podrás acceder a este link dentro de este día en curso.
</p>
"""