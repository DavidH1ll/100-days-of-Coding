"""
Day 58: Bootstrap Framework Learning
Flask app to serve Bootstrap example pages
"""

from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    """Home page with links to all examples"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Day 58: Bootstrap Learning</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 50px 0;
            }
            .card {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }
            .btn-custom {
                width: 100%;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    <div class="card shadow-lg">
                        <div class="card-header bg-primary text-white">
                            <h1 class="text-center mb-0">🎓 Day 58: Bootstrap Framework</h1>
                        </div>
                        <div class="card-body">
                            <p class="lead text-center">
                                Explore Bootstrap's powerful features through interactive examples
                            </p>
                            
                            <div class="row mt-4">
                                <!-- Introduction Card -->
                                <div class="col-md-6 mb-4">
                                    <div class="card h-100">
                                        <div class="card-body">
                                            <h5 class="card-title">🌻 Bootstrap Introduction</h5>
                                            <p class="card-text">
                                                Learn the basics of Bootstrap with a beautiful card component example.
                                                See how easy it is to create professional-looking designs!
                                            </p>
                                            <a href="/bootstrap_intro" class="btn btn-primary btn-custom">
                                                View Introduction
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Layout Examples Card -->
                                <div class="col-md-6 mb-4">
                                    <div class="card h-100">
                                        <div class="card-body">
                                            <h5 class="card-title">📐 12-Column Layout System</h5>
                                            <p class="card-text">
                                                Explore Bootstrap's powerful grid system with multiple examples 
                                                showing different column configurations and responsive behaviors.
                                            </p>
                                            <a href="/layout_examples" class="btn btn-primary btn-custom">
                                                View Layout Examples
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Exercise 1 Card -->
                                <div class="col-md-4 mb-4">
                                    <div class="card h-100 border-success">
                                        <div class="card-body">
                                            <h5 class="card-title">💻 Exercise 1</h5>
                                            <p class="card-text">
                                                Desktop 50%, Mobile 100% responsive layout challenge.
                                            </p>
                                            <a href="/exercise1" class="btn btn-success btn-custom">
                                                Start Exercise 1
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Exercise 2 Card -->
                                <div class="col-md-4 mb-4">
                                    <div class="card h-100 border-warning">
                                        <div class="card-body">
                                            <h5 class="card-title">📱 Exercise 2</h5>
                                            <p class="card-text">
                                                Three-column multi-breakpoint responsive layout challenge.
                                            </p>
                                            <a href="/exercise2" class="btn btn-warning btn-custom">
                                                Start Exercise 2
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Exercise 3 Card -->
                                <div class="col-md-4 mb-4">
                                    <div class="card h-100 border-danger">
                                        <div class="card-body">
                                            <h5 class="card-title">🎯 Exercise 3</h5>
                                            <p class="card-text">
                                                Dynamic sidebar with proportions changing across all breakpoints.
                                            </p>
                                            <a href="/exercise3" class="btn btn-danger btn-custom">
                                                Start Exercise 3
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row mt-4">
                                <!-- Components Showcase Card -->
                                <div class="col-md-6 mb-4">
                                    <div class="card h-100 border-info">
                                        <div class="card-body">
                                            <h5 class="card-title">🎨 Components Showcase</h5>
                                            <p class="card-text">
                                                Explore all major Bootstrap components: buttons, alerts, cards, 
                                                accordions, progress bars, and more!
                                            </p>
                                            <a href="/components" class="btn btn-info btn-custom">
                                                View Components
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Complete Website Card -->
                                <div class="col-md-6 mb-4">
                                    <div class="card h-100 border-primary">
                                        <div class="card-body">
                                            <h5 class="card-title">🌐 Complete Website Example</h5>
                                            <p class="card-text">
                                                See everything together! Full website with navbar, hero, features, 
                                                carousel, pricing, contact form, and footer. Includes dark mode!
                                            </p>
                                            <a href="/complete_website" class="btn btn-primary btn-custom">
                                                View Complete Site
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row mt-4">
                                <!-- TinDog Project Card -->
                                <div class="col-12">
                                    <div class="card border-danger">
                                        <div class="card-body">
                                            <h3 class="card-title">🐕 Day 58 Project: TinDog Startup Website</h3>
                                            <p class="card-text">
                                                <strong>The Main Project!</strong> Build a complete startup landing page for TinDog - 
                                                Tinder for dogs! Features animated gradient background, hero section, features, 
                                                testimonials, pricing plans, and footer. This project combines everything you've 
                                                learned about Bootstrap components and layouts.
                                            </p>
                                            <a href="/tindog" class="btn btn-danger btn-lg btn-custom">
                                                🚀 Launch TinDog Project
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="alert alert-info mt-4">
                                <h5>📚 Learning Resources</h5>
                                <ul class="mb-0">
                                    <li><a href="https://getbootstrap.com" target="_blank">Bootstrap Official Documentation</a></li>
                                    <li><a href="https://getbootstrap.com/docs/5.3/layout/grid/" target="_blank">Grid System Documentation</a></li>
                                    <li><a href="https://getbootstrap.com/docs/5.3/layout/breakpoints/" target="_blank">Breakpoints Guide</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="card-footer text-muted text-center">
                            <small>Day 58 of 100 Days of Coding Challenge</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """


@app.route('/bootstrap_intro')
def bootstrap_intro():
    """Serve the Bootstrap introduction page"""
    return send_from_directory(BASE_DIR, 'bootstrap_intro.html')


@app.route('/layout_examples')
def layout_examples():
    """Serve the layout examples page"""
    return send_from_directory(BASE_DIR, 'layout_examples.html')


@app.route('/exercise1')
def exercise1():
    """Serve exercise 1 page"""
    return send_from_directory(BASE_DIR, 'exercise1.html')


@app.route('/exercise2')
def exercise2():
    """Serve exercise 2 page"""
    return send_from_directory(BASE_DIR, 'exercise2.html')


@app.route('/exercise3')
def exercise3():
    """Serve exercise 3 page"""
    return send_from_directory(BASE_DIR, 'exercise3.html')


@app.route('/components')
def components():
    """Serve components showcase page"""
    return send_from_directory(BASE_DIR, 'components_showcase.html')


@app.route('/complete_website')
def complete_website():
    """Serve complete website example"""
    return send_from_directory(BASE_DIR, 'complete_website.html')


@app.route('/tindog')
def tindog():
    """Serve TinDog project page"""
    return send_from_directory(BASE_DIR, 'tindog_project.html')


@app.route('/tindog_style.css')
def tindog_css():
    """Serve TinDog CSS"""
    return send_from_directory(BASE_DIR, 'tindog_style.css')


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Day 58: Bootstrap Framework Learning")
    print("="*60)
    print("\n📖 Available Pages:")
    print("   • Home:             http://localhost:5000/")
    print("   • Introduction:     http://localhost:5000/bootstrap_intro")
    print("   • Layout Examples:  http://localhost:5000/layout_examples")
    print("   • Exercise 1:       http://localhost:5000/exercise1")
    print("   • Exercise 2:       http://localhost:5000/exercise2")
    print("   • Exercise 3:       http://localhost:5000/exercise3")
    print("   • Components:       http://localhost:5000/components")
    print("   • Complete Site:    http://localhost:5000/complete_website")
    print("   • 🐕 TinDog Project: http://localhost:5000/tindog")
    print("\n💡 Tip: Resize your browser or use Chrome DevTools device")
    print("   toolbar to see responsive behavior in action!")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
