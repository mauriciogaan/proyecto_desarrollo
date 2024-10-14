
install.packages(c("sf", "ggplot2", "rnaturalearth", "rnaturalearthdata"))


library(sf)
library(ggplot2)
library(rnaturalearth)
library(rnaturalearthdata)
library(readxl)

#Cargar Datos
path <- "/Users/mauga/Desktop/desarrollo/intermediates/fgt1_por_ubicacion_actualizada.xlsx"
mexico_map <- ne_states(country = "Mexico", returnclass = "sf")
fgt1_data <- read_excel(path)
names(fgt1_data )[1] <- "name"

#Mapa
mexico_map <- merge(mexico_map, fgt1_data, by.x = "name", by.y = "name")
mexico_map$fgt1 <- fgt1_data$fgt1 * 100
mapa_fgt1 <- ggplot(mexico_map) +
  geom_sf(aes(fill = fgt1), color = "black") +
  scale_fill_gradient(low = "#ffcccc", high = "#990000", name = "FGT1 (%)") +  # Paleta de rojos
  theme_minimal() +
  labs(title = "") +
  theme(
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    panel.grid = element_blank()
  ) +
  geom_sf_text(aes(label = name), size = 3, color = "black")
mapa_fgt1
ggsave("/Users/mauga/Desktop/desarrollo/outcomes/mapa_fgt1_pobreza.png", plot = mapa_fgt1, width = 15, height = 10)
