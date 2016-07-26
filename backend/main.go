package main

import (
    "github.com/gin-gonic/gin"
    "github.com/olahol/go-imageupload"
    "net/http"
    "time"
    "fmt"
)

//  s := fmt.Sprintf("%s.png", time.Now().Format("2006_01_02_15_04_05"))


func image_upload(c *gin.Context) {
    img, err := imageupload.Process(c.Request, "file")

    if err != nil {
        //TODO fix
        panic(err)
    }

    img.Save(fmt.Sprintf("%d.jpg", time.Now().Unix()))

    c.Redirect(http.StatusMovedPermanently, "/")
}

func main() {

    r := gin.Default()

    r.GET("/", func(c *gin.Context) {
        c.File("index.html")
    })

    r.POST("/upload", image_upload)

    r.Run(":5000")
}

