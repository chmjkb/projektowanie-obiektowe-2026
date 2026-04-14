package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/labstack/echo/v4"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// Weather is a GORM model representing a city with its coordinates
type Weather struct {
	gorm.Model
	City      string  `json:"city" gorm:"uniqueIndex"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
}

// WeatherResponse represents weather data returned by our API
type WeatherResponse struct {
	City        string  `json:"city"`
	Temperature float64 `json:"temperature"`
	Description string  `json:"description"`
}

// OpenMeteoResponse represents the response from Open-Meteo API
type OpenMeteoResponse struct {
	CurrentWeather struct {
		Temperature float64 `json:"temperature"`
		WeatherCode int     `json:"weathercode"`
	} `json:"current_weather"`
}

// WeatherProxy fetches weather data from external Open-Meteo API
type WeatherProxy struct{}

func (p *WeatherProxy) FetchWeather(lat, lon float64) (*OpenMeteoResponse, error) {
	url := fmt.Sprintf("https://api.open-meteo.com/v1/forecast?latitude=%f&longitude=%f&current_weather=true", lat, lon)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result OpenMeteoResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return &result, nil
}

// weatherCodeToDescription converts Open-Meteo weather code to description
func weatherCodeToDescription(code int) string {
	switch {
	case code == 0:
		return "Clear sky"
	case code <= 3:
		return "Partly cloudy"
	case code <= 49:
		return "Foggy"
	case code <= 59:
		return "Drizzle"
	case code <= 69:
		return "Rain"
	case code <= 79:
		return "Snow"
	case code <= 99:
		return "Thunderstorm"
	default:
		return "Unknown"
	}
}

var proxy = &WeatherProxy{}
var db *gorm.DB

// initDB initializes the database and loads initial data
func initDB() {
	var err error
	db, err = gorm.Open(sqlite.Open("weather.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	// Auto migrate the schema
	db.AutoMigrate(&Weather{})

	// Load initial data from list
	cities := []Weather{
		{City: "Warsaw", Latitude: 52.2297, Longitude: 21.0122},
		{City: "Krakow", Latitude: 50.0647, Longitude: 19.9450},
		{City: "Gdansk", Latitude: 54.3520, Longitude: 18.6466},
		{City: "Wroclaw", Latitude: 51.1079, Longitude: 17.0385},
		{City: "Poznan", Latitude: 52.4064, Longitude: 16.9252},
	}

	for _, city := range cities {
		db.FirstOrCreate(&city, Weather{City: city.City})
	}
}

func main() {
	initDB()

	e := echo.New()

	// Weather controller endpoint
	e.GET("/weather", getWeather)

	e.Logger.Fatal(e.Start(":8080"))
}

// getWeather returns weather data for a given city
func getWeather(c echo.Context) error {
	cityName := c.QueryParam("city")
	if cityName == "" {
		cityName = "Warsaw"
	}

	// Look up city in database
	var city Weather
	result := db.Where("city = ?", cityName).First(&city)
	if result.Error != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": "City not found in database"})
	}

	// Fetch weather from external API via proxy
	data, err := proxy.FetchWeather(city.Latitude, city.Longitude)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}

	weather := WeatherResponse{
		City:        city.City,
		Temperature: data.CurrentWeather.Temperature,
		Description: weatherCodeToDescription(data.CurrentWeather.WeatherCode),
	}

	return c.JSON(http.StatusOK, weather)
}
