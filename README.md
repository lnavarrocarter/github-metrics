# GitHub Metrics Service

Servicio propio para generar tarjetas SVG de métricas públicas de GitHub. Está diseñado para ejecutarse en Cloud Run y evitar la dependencia de tarjetas públicas de terceros.

## Endpoints

### Perfil propio (sin whitelist, usa `GITHUB_USERNAME`)

| Ruta | Métrica |
| --- | --- |
| `/metrics/overview.svg` | Repositorios, seguidores, estrellas y forks. |
| `/metrics/languages.svg` | Lenguajes predominantes por repositorio. |
| `/metrics/activity.svg` | Eventos públicos recientes: pushes, pull requests e issues. |
| `/metrics/pulse.svg` | Salud del portafolio: proyectos activos, actividad y archivados. |

### Multi-perfil (requiere whitelist)

```
/cards/github/<username>/overview.svg
/cards/github/<username>/languages.svg
/cards/github/<username>/activity.svg
/cards/github/<username>/pulse.svg
```

Todas las rutas aceptan `?theme=` con uno de: `tokyonight` (default), `sunset`, `forest`, `mono`.

### Instagram y LinkedIn

```
/cards/instagram/<username>/overview.svg
/cards/linkedin/<username>/overview.svg
```

Ninguna de las dos plataformas ofrece una API pública para leer métricas de perfiles de terceros en vivo (Instagram exige una cuenta Business/Creator vinculada a una Página de Meta con OAuth propio; LinkedIn no tiene API pública de métricas de perfil para terceros). En vez de hacer scraping —que violaría sus términos de servicio y sería poco confiable— estas tarjetas muestran **datos auto-reportados por el propio dueño del perfil**, guardados en [config/profiles.json](config/profiles.json) y marcados explícitamente como "manual" (nunca se presentan como datos en vivo). Si tu usuario está en la whitelist pero no tiene datos cargados, la tarjeta muestra "pendiente" en vez de un error.

## Whitelist: cómo sumar tu perfil

El servicio es multi-tenant pero cerrado por whitelist: sólo usuarios listados en [config/whitelist.json](config/whitelist.json) pueden generar tarjetas vía `/cards/<platform>/<username>/...`. Para sumarte:

1. Haz un fork y abre un PR agregando tu usuario al arreglo del `platform` correspondiente (`github`, `instagram` o `linkedin`) en `config/whitelist.json`.
2. Si es Instagram o LinkedIn, agrega también tus propios datos (nombre, handle, seguidores/conexiones, fecha) en `config/profiles.json` bajo tu usuario — nadie carga datos de otra persona.
3. Un mantenedor revisa y aprueba el PR (evita abuso y controla el consumo de la API de GitHub).
4. Una vez mergeado y desplegado, usa `/cards/<platform>/<tu-usuario>/<tarjeta>.svg` en tu propio README.

Un usuario fuera de la whitelist recibe una tarjeta 403 "Acceso no autorizado", nunca un error genérico.

Las próximas métricas priorizadas son una racha de contribuciones basada en GraphQL, releases publicados, PRs fusionados y un resumen anual. Están listadas como trabajo pendiente en [TASKS.md](TASKS.md).

## Desarrollo local

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GITHUB_USERNAME = "lnavarrocarter"
$env:GITHUB_TOKEN = "<token-fine-grained-read-only>"
flask --app app.main run
```

Abre `http://127.0.0.1:5000/metrics/overview.svg`.

## Despliegue en GCP

1. Crea un proyecto de GCP, habilita Cloud Run, Cloud Build, Artifact Registry, Secret Manager e IAM Credentials API.
2. Crea el secreto `github-metrics-token` con un Fine-grained PAT de GitHub, permisos de sólo lectura para metadatos y repositorios públicos.
3. Configura Workload Identity Federation para GitHub Actions y otorga al service account `roles/run.admin`, `roles/iam.serviceAccountUser`, `roles/cloudbuild.builds.editor` y `roles/secretmanager.secretAccessor`.
4. En GitHub, crea las variables `GCP_PROJECT_ID` y `GCP_REGION`, y los secretos `GCP_WORKLOAD_IDENTITY_PROVIDER` y `GCP_SERVICE_ACCOUNT`.
5. Haz push a `main`; el workflow publica el servicio. Asocia después `metrics.navarrocarter.com` mediante un external Application Load Balancer con certificado gestionado.

El token nunca se expone en la respuesta SVG ni en Git. Cloud Run lo toma desde Secret Manager y las respuestas se cachean durante una hora.
