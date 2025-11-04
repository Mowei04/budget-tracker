from app import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)  # 仅本地开发；部署时不要直接用 app.run【14】