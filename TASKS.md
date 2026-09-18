# Tareas

## Inicial

- [x] Servicio Flask que genera SVG bajo control propio.
- [x] Tarjetas de resumen, lenguajes, actividad y pulso de open source.
- [x] Caché en proceso de una hora y cabeceras cacheables para CDN.
- [x] Contenedor para Cloud Run y workflow de despliegue con Workload Identity Federation.
- [x] Pruebas unitarias de renderizado SVG.

## Antes de producción

- [ ] Crear el repositorio `lnavarrocarter/github-metrics` y subir este directorio como su raíz.
- [ ] Crear el proyecto GCP, APIs, service account, identidad federada y secretos indicados en el README.
- [ ] Desplegar y registrar la URL de Cloud Run o el dominio `metrics.navarrocarter.com`.
- [ ] Actualizar las imágenes externas del README de perfil para que usen los endpoints propios.
- [ ] Añadir límites por IP o Cloud Armor si se expone el servicio más allá del README.

## Multi-tenant, temas y animaciones (hecho)

- [x] Sistema de temas (`tokyonight`, `sunset`, `forest`, `mono`) vía `?theme=`.
- [x] Animaciones SVG nativas (SMIL): borde con brillo en movimiento, punto "en vivo" pulsante, barras de lenguaje que crecen al cargar.
- [x] Rutas multi-perfil `/cards/github/<username>/<card>.svg` protegidas por whitelist en `config/whitelist.json`.
- [x] Tarjetas de error/acceso denegado con el mismo sistema de temas (nunca un SVG roto).
- [x] Arquitectura de rutas lista para otras plataformas (`/cards/<platform>/<username>/...`).

## Instagram y LinkedIn (bloqueado por plataforma, no por diseño)

- [ ] Instagram: requiere que cada usuario conecte una cuenta Business/Creator vía Meta Graph API (OAuth propio, token de larga duración). No es posible leer métricas de un perfil ajeno sin ese consentimiento explícito.
- [ ] LinkedIn: no expone una API pública de métricas de perfil para terceros; cualquier alternativa implicaría scraping, lo cual viola sus términos de servicio y es inestable.
- [ ] Alternativa intermedia: permitir que cada usuario registre manualmente sus propios números (seguidores, conexiones) vía PR a un JSON firmado por ellos mismos, renderizados con el mismo sistema de temas — sin pretender ser "en vivo".

## Métricas siguientes (GitHub)

- [ ] Racha y mapa anual de contribuciones usando GitHub GraphQL `contributionsCollection`.
- [ ] Releases y versiones más recientes por repositorio.
- [ ] Pull requests creados, fusionados y tiempo medio de merge.
- [ ] Issues abiertos/cerrados y porcentaje de resolución.
- [ ] Distribución de lenguajes por bytes de código, no sólo por cantidad de repositorios.
- [ ] Tendencia de estrellas y forks con snapshots diarios en BigQuery o Firestore.
- [ ] Tarjeta de impacto: usuarios, organizaciones y repositorios destacados.
- [ ] Vista JSON protegida para alimentar una web personal o un dashboard interno.
- [ ] Rate limiting por IP/usuario en `/cards/...` para proteger la cuota de la API de GitHub compartida entre todos los usuarios whitelisteados.
