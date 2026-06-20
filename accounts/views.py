from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SignupSerializer
from .models import User


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Account created successfully!'},
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email,
        'college_email': user.college_email,
        'campus': user.campus,
        'major': user.major,
        'graduation_year': user.graduation_year,
        'bio': user.bio,
        'avatar': user.avatar.url if user.avatar else None,
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user
    user.campus = request.data.get('campus', user.campus)
    user.major = request.data.get('major', user.major)
    user.bio = request.data.get('bio', user.bio)
    user.graduation_year = request.data.get('graduation_year', user.graduation_year)
    if 'avatar' in request.FILES:
        user.avatar = request.FILES['avatar']
    user.save()
    return Response({
        'message': 'Profile updated successfully!',
        'username': user.username,
        'campus': user.campus,
        'major': user.major,
        'bio': user.bio,
        'graduation_year': user.graduation_year,
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response(
        {'message': 'Account deleted successfully!'},
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            username__icontains=query
        ) | User.objects.filter(
            campus__icontains=query
        ) | User.objects.filter(
            major__icontains=query
        )
        results = []
        for user in users:
            results.append({
                'username': user.username,
                'campus': user.campus,
                'major': user.major,
                'graduation_year': user.graduation_year,
            })
        return Response(results)
    return Response([])


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if target_user == request.user:
        return Response({'message': 'You cannot follow yourself'},
                       status=status.HTTP_400_BAD_REQUEST)

    if request.user in target_user.followers.all():
        target_user.followers.remove(request.user)
        return Response({'message': 'Unfollowed'})
    else:
        target_user.followers.add(request.user)
        return Response({'message': 'Followed'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request, username):
    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response({
        'username': target_user.username,
        'campus': target_user.campus,
        'major': target_user.major,
        'followers_count': target_user.followers.count(),
        'following_count': target_user.following.count(),
        'is_following': request.user in target_user.followers.all()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followers_list(request):
    user = request.user
    followers = user.followers.all()
    results = []
    for f in followers:
        results.append({
            'username': f.username,
            'campus': f.campus,
            'major': f.major,
            'avatar': f.avatar.url if f.avatar else None,
        })
    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following_list(request):
    user = request.user
    following = user.following.all()
    results = []
    for f in following:
        results.append({
            'username': f.username,
            'campus': f.campus,
            'major': f.major,
            'avatar': f.avatar.url if f.avatar else None,
        })
    return Response(results)