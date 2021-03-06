package middlewares

import (
	"github.com/DemoHn/obsidian-panel/infra"
	"github.com/labstack/echo"

	"github.com/go-playground/validator"
)

// ErrorHandler - new Error middleware
func ErrorHandler() echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			if err := next(c); err != nil {
				// wrap errors to export
				var wrapError *infra.Error

				switch e := err.(type) {
				case *infra.Error:
					wrapError = e
				case *echo.HTTPError:
					wrapError = infra.GeneralHTTPError(e.Code, e.Message)
				case validator.ValidationErrors:
					wrapError = infra.ValidationError(err)
				default:
					wrapError = infra.UnknownServerError(err)
				}

				return c.JSON(wrapError.StatusCode, wrapError)
			}
			return nil
		}
	}
}
