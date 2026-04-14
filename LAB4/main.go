package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/labstack/echo/v4"
)

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

func main() {
	e := echo.New()

	// Weather controller endpoint
	e.GET("/weather", getWeather)

	e.Logger.Fatal(e.Start(":8080"))
}

// getWeather returns weather data for a given city (using coordinates)
func getWeather(c echo.Context) error {
	city := c.QueryParam("city")
	if city == "" {
		city = "Warsaw"
	}

	// Default coordinates for Warsaw
	lat := 52.2297
	lon := 21.0122

	// Fetch weather from external API via proxy
	data, err := proxy.FetchWeather(lat, lon)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}

	weather := WeatherResponse{
		City:        city,
		Temperature: data.CurrentWeather.Temperature,
		Description: weatherCodeToDescription(data.CurrentWeather.WeatherCode),
	}

	return c.JSON(http.StatusOK, weather)
}
