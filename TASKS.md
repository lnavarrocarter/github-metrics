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

## Métricas siguientes

- [ ] Racha y mapa anual de contribuciones usando GitHub GraphQL `contributionsCollection`.
- [ ] Releases y versiones más recientes por repositorio.
- [ ] Pull requests creados, fusionados y tiempo medio de merge.
- [ ] Issues abiertos/cerrados y porcentaje de resolución.
- [ ] Distribución de lenguajes por bytes de código, no sólo por cantidad de repositorios.
- [ ] Tendencia de estrellas y forks con snapshots diarios en BigQuery o Firestore.
- [ ] Tarjeta de impacto: usuarios, organizaciones y repositorios destacados.
- [ ] Vista JSON protegida para alimentar una web personal o un dashboard interno.
