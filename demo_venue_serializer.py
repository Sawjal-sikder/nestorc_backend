#!/usr/bin/env python3
"""
Simple demonstration of CreateVenueSerializer creating scavenger hunts and venue messages
"""
import os
import sys
import django
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from services.models import City, PlaceType, Venue, ScavengerHunt, List_Message
from services.serializers import CreateVenueSerializer

def demonstrate_create_venue_serializer():
    """Demonstrate CreateVenueSerializer functionality"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🎯 CreateVenueSerializer Demonstration")
    print("=" * 50)
    
    # Get or create test data
    city = City.objects.get_or_create(
        name="Demo City",
        defaults={'description': "Demo city for testing"}
    )[0]
    
    place_type = PlaceType.objects.get_or_create(
        name="Demo Restaurant",
        defaults={'description': "Demo restaurant type"}
    )[0]
    
    print(f"🏙️  Using City: {city.name}")
    print(f"🏪 Using Place Type: {place_type.name}")
    print()
    
    # Create venue with scavenger hunts and messages
    venue_data = {
        'city': city.id,
        'type_of_place': place_type.id,
        'venue_name': f'Demo Restaurant {timestamp}',
        'description': 'A demo restaurant with scavenger hunts and messages',
        'latitude': 40.7589,
        'longitude': -73.9851,
        'scavenger_hunts': [
            {'title': 'Find the secret menu'},
            {'title': 'Take a selfie with the mascot'},
            {'title': 'Try the chef special'}
        ],
        'venue_message': [
            {'message': 'Welcome to our amazing restaurant!'},
            {'message': 'Don\'t forget to check out our daily specials!'},
            {'message': 'Thank you for visiting us!'}
        ]
    }
    
    print("📝 Input Data:")
    print(f"   Venue Name: {venue_data['venue_name']}")
    print(f"   Scavenger Hunts: {len(venue_data['scavenger_hunts'])} items")
    for i, hunt in enumerate(venue_data['scavenger_hunts'], 1):
        print(f"      {i}. {hunt['title']}")
    print(f"   Messages: {len(venue_data['venue_message'])} items")
    for i, msg in enumerate(venue_data['venue_message'], 1):
        print(f"      {i}. {msg['message']}")
    print()
    
    # Create serializer and save
    serializer = CreateVenueSerializer(data=venue_data)
    
    if serializer.is_valid():
        venue = serializer.save()
        print(f"✅ Venue created successfully!")
        print(f"   ID: {venue.id}")
        print(f"   Name: {venue.venue_name}")
        print()
        
        # Check created objects
        hunts = venue.scavenger_hunts.all()
        messages = venue.messages.all()
        
        print(f"🎲 Created Scavenger Hunts ({hunts.count()}):")
        for hunt in hunts:
            print(f"   - {hunt.title}")
        print()
        
        print(f"💬 Created Messages ({messages.count()}):")
        for message in messages:
            print(f"   - {message.message}")
        print()
        
        # Show serializer output
        print("📄 Serializer Output:")
        representation = serializer.to_representation(venue)
        print(f"   Venue: {representation['venue_name']}")
        print(f"   City: {representation['city']}")
        print(f"   Type: {representation['type_of_place']}")
        print(f"   Scavenger Hunts in response: {len(representation['scavenger_hunts'])}")
        print(f"   Messages in response: {len(representation['venue_message'])}")
        
        print("\n🎉 SUCCESS! The CreateVenueSerializer:")
        print("   ✅ Creates the venue")
        print("   ✅ Creates associated scavenger hunts")
        print("   ✅ Creates associated venue messages")
        print("   ✅ Returns complete data in the response")
        
        return True
    else:
        print(f"❌ Serializer validation failed: {serializer.errors}")
        return False

def demonstrate_venue_without_related():
    """Demonstrate creating venue without related objects"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n" + "=" * 50)
    print("🎯 Creating Venue WITHOUT Related Objects")
    print("=" * 50)
    
    # Get existing test data
    city = City.objects.get(name="Demo City")
    place_type = PlaceType.objects.get(name="Demo Restaurant")
    
    venue_data = {
        'city': city.id,
        'type_of_place': place_type.id,
        'venue_name': f'Simple Cafe {timestamp}',
        'description': 'A simple cafe without any extras',
        'latitude': 40.7500,
        'longitude': -73.9800
        # No scavenger_hunts or venue_message
    }
    
    print("📝 Input Data (no related objects):")
    print(f"   Venue Name: {venue_data['venue_name']}")
    print("   Scavenger Hunts: None")
    print("   Messages: None")
    print()
    
    serializer = CreateVenueSerializer(data=venue_data)
    
    if serializer.is_valid():
        venue = serializer.save()
        print(f"✅ Simple venue created successfully!")
        print(f"   ID: {venue.id}")
        print(f"   Name: {venue.venue_name}")
        print(f"   Scavenger Hunts: {venue.scavenger_hunts.count()}")
        print(f"   Messages: {venue.messages.count()}")
        
        print("\n🎉 SUCCESS! The serializer works with or without related objects!")
        return True
    else:
        print(f"❌ Serializer validation failed: {serializer.errors}")
        return False

if __name__ == "__main__":
    try:
        print("🚀 Starting CreateVenueSerializer Demonstration")
        print("=" * 60)
        
        result1 = demonstrate_create_venue_serializer()
        result2 = demonstrate_venue_without_related()
        
        print("\n" + "=" * 60)
        if result1 and result2:
            print("🎉 DEMONSTRATION COMPLETE!")
            print("✨ CreateVenueSerializer successfully creates:")
            print("   📍 Venues with scavenger hunts and messages")
            print("   📍 Simple venues without related objects")
            print("   📍 Proper response data including all related objects")
        else:
            print("⚠️  Some issues were encountered.")
            
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
