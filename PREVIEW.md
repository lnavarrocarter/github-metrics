# Vista previa y guía de uso

Este documento sirve para dos cosas: **ver de un vistazo** lo que genera el servicio hoy (con mis propios perfiles como caso de prueba) y **documentar cómo usarlo** si quieres sumar tu perfil.

> Las imágenes se cargan en vivo desde Cloud Run (`https://github-metrics-306971032277.us-central1.run.app`). Si ves un rectángulo roto es porque tu editor/visor de Markdown no carga imágenes remotas, no porque el servicio esté caído.

## GitHub — perfil propio (`lnavarrocarter`)

Ruta base: `/metrics/<card>.svg` (sin whitelist, usa el usuario configurado en `GITHUB_USERNAME`).

| Tarjeta | Vista previa |
| --- | --- |
| `overview` | ![overview](https://github-metrics-306971032277.us-central1.run.app/metrics/overview.svg) |
| `languages` | ![languages](https://github-metrics-306971032277.us-central1.run.app/metrics/languages.svg) |
| `activity` | ![activity](https://github-metrics-306971032277.us-central1.run.app/metrics/activity.svg) |
| `pulse` | ![pulse](https://github-metrics-306971032277.us-central1.run.app/metrics/pulse.svg) |

## GitHub — ruta multi-perfil (`/cards/github/<username>/...`)

La misma tarjeta `overview`, para `lnavarrocarter`, pasando por la whitelist:

![overview multi-tenant](https://github-metrics-306971032277.us-central1.run.app/cards/github/lnavarrocarter/overview.svg)

## Temas disponibles

Todas las rutas aceptan `?theme=`. Ejemplo con `overview`:

| Tema | Vista previa |
| --- | --- |
| `tokyonight` (default) | ![tokyonight](https://github-metrics-306971032277.us-central1.run.app/metrics/overview.svg?theme=tokyonight) |
| `sunset` | ![sunset](https://github-metrics-306971032277.us-central1.run.app/metrics/overview.svg?theme=sunset) |
| `forest` | ![forest](https://github-metrics-306971032277.us-central1.run.app/metrics/overview.svg?theme=forest) |
| `mono` | ![mono](https://github-metrics-306971032277.us-central1.run.app/metrics/overview.svg?theme=mono) |

## Instagram y LinkedIn (datos auto-reportados)

Estas tarjetas **no son en vivo**: muestran los datos que cada usuario carga manualmente en `config/profiles.json`, marcados con el indicador "manual" en vez del punto pulsante "en vivo" de GitHub. Ver la sección "Por qué no hay datos en vivo" en el [README](README.md) para el detalle técnico de por qué no se puede hacer scraping.

| Plataforma | Vista previa |
| --- | --- |
| Instagram (`lnavarrocarter`) | ![instagram](https://github-metrics-306971032277.us-central1.run.app/cards/instagram/lnavarrocarter/overview.svg) |
| LinkedIn (`lnavarrocarter`) | ![linkedin](https://github-metrics-306971032277.us-central1.run.app/cards/linkedin/lnavarrocarter/overview.svg) |

Los campos `followers`, `posts` y `connections` de mi perfil todavía están en `null` en `config/profiles.json` — por eso ves `—` en vez de un número. Actualízalos ahí cuando quieras.

## Casos de error (para saber qué esperar)

| Caso | Ruta de ejemplo | Vista previa |
| --- | --- | --- |
| Usuario no whitelisteado (403) | `/cards/github/usuario-no-registrado/overview.svg` | ![403](https://github-metrics-306971032277.us-central1.run.app/cards/github/usuario-no-registrado/overview.svg) |
| Plataforma no soportada (404) | `/cards/tiktok/lnavarrocarter/overview.svg` | ![404](https://github-metrics-306971032277.us-central1.run.app/cards/tiktok/lnavarrocarter/overview.svg) |
| Perfil whitelisteado sin datos cargados | `/cards/instagram/<usuario-sin-profiles.json>/overview.svg` | Tarjeta "pendiente", mismo estilo que las demás. |

## Cómo usar tu propia tarjeta en un README

```markdown
![Mis métricas de GitHub](https://github-metrics-306971032277.us-central1.run.app/cards/github/tu-usuario/overview.svg?theme=sunset)
```

Pasos:

1. Verifica que tu usuario de GitHub esté en `config/whitelist.json` (bajo `github`). Si no está, abre un PR agregándolo.
2. Si quieres tarjetas de Instagram/LinkedIn, agrega tu usuario en `whitelist.json` bajo esa plataforma **y** tus propios datos en `config/profiles.json` (nadie carga datos de otra persona).
3. Copia el `<img>`/`![]()` con tu usuario y el tema que prefieras en tu README.
4. Espera el `Cache-Control: max-age=3600`: las tarjetas se refrescan como máximo cada hora.

## Endpoints de referencia rápida

```
/status
/metrics/<overview|languages|activity|pulse>.svg
/cards/github/<username>/<overview|languages|activity|pulse>.svg
/cards/instagram/<username>/overview.svg
/cards/linkedin/<username>/overview.svg
```

Todos aceptan `?theme=tokyonight|sunset|forest|mono`.
