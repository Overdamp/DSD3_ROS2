from setuptools import find_packages, setup

package_name = 'AI_object_detection'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='luke',
    maintainer_email='luke@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'collect_data = AI_object_detection.collect_data_node:main',
            'detect_object = AI_object_detection.object_detection_node:main',
            'yolo_world = AI_object_detection.yolo_world_node:main'
        ],
    },
)
