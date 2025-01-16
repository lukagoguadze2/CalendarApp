export async function fetchCourseSchedule() {
    try {
        // Make the API request
        const baseUrl = window.location.origin;
        const response = await fetch(baseUrl + '/api/schedules/courses/my_course_schedule/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Check for successful response
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse JSON response
        const inputJson = await response.json();
        const SemesterStartTime = new Date(2024, 8, 21);
        // Transform data into desired format
        const results = inputJson.map((item) => {
            let events = [];

            for (let i = 0; i < item.course.duration_in_weeks; i++) {
                // Calculate the start date for each week
                const startDate = new Date(SemesterStartTime);
                startDate.setDate(SemesterStartTime.getDate() + i * 7);

                //
                // FIX: fix me pls
                //

                const startTime = `${startDate.toISOString().split('T')[0]}T${item.schedule.start_time}.000Z`;
                const endTime = `${startDate.toISOString().split('T')[0]}T${item.schedule.end_time}.000Z`;

                console.log(startDate);

                events.push({
                    groupId: item.group.id.toString(),
                    title: item.description,
                    start: startTime,
                    end: endTime,
                    color: '#5baa73',
                });
            }
            return events;
        });

        let LastResults = [];
        results.forEach((result) => {
            result.forEach((event) => {
                LastResults.push(event);
            });
        });
        console.log('Processed Results:', LastResults);
        return LastResults;
    } catch (error) {
        console.error('Error fetching course schedule:', error);
    }
}