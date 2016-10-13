package main

import (
    "github.com/gin-gonic/gin"
    "github.com/olahol/go-imageupload"
    "net/http"
    "time"
    "fmt"
    "database/sql"
    _ "github.com/mattn/go-sqlite3"
)

//  s := fmt.Sprintf("%s.png", time.Now().Format("2006_01_02_15_04_05"))

var db *sql.DB

func image_upload(c *gin.Context) {
    img, err := imageupload.Process(c.Request, "file")

    if err != nil {
        //TODO fix
        panic(err)
    }

    fname := fmt.Sprintf("images/%d.jpg", time.Now().Unix())
//      img.Save(fmt.Sprintf("%d.jpg", time.Now().Unix()))
    img.Save(fname)
    query := "insert into images(path) values(?)"
    _, err = db.Exec(query, "/" + fname)
    if err != nil {
        panic(err)
    }

    c.Redirect(http.StatusMovedPermanently, "/")
}

func main() {
    // prepare for DB

    var err error
    db, err = sql.Open("sqlite3", "./data.db")
    if err != nil {
        panic(err)
    }
    r := gin.Default()
    r.LoadHTMLGlob("template/*.tmpl")

    r.GET("/", func(c *gin.Context) {
        query := `select count(1) from images`
        rows, err := db.Query(query)
        if err != nil {
            panic(err)
        }
        defer rows.Close()
        count := 0
        for rows.Next() {
            err = rows.Scan(&count)
            if err != nil {
                panic(err)
            }
        }

        query = "select path from images order by id desc limit 10"
        rows, err = db.Query(query)
        if err != nil {
            panic(err)
        }
        defer rows.Close()
        images := []string{}
        for rows.Next() {
            var path string
            err = rows.Scan(&path)
            if err != nil {
                panic(err)
            }
            images = append(images, path)
        }

        c.HTML(http.StatusOK, "show_image.tmpl",
            gin.H{"count": count, "images": images})
    })

    r.POST("/upload", image_upload)

    r.Run(":5000")
}

