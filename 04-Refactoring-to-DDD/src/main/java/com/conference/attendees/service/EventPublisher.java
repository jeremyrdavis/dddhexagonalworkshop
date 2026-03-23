package com.conference.attendees.service;

import com.conference.attendees.model.AttendeeEntity;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Event;
import jakarta.inject.Inject;
import java.util.logging.Logger;

/**
 * Traditional event publisher using CDI events.
 * This will be refactored to use proper domain events later.
 */
@ApplicationScoped
public class EventPublisher {

    private static final Logger logger = Logger.getLogger(EventPublisher.class.getName());

    @Inject
    private Event<AttendeeRegistrationEvent> attendeeRegistrationEvent;

    public void publishAttendeeRegisteredEvent(AttendeeEntity attendee) {
        logger.info("Publishing attendee registered event for: " + attendee.getEmail());

        AttendeeRegistrationEvent event = new AttendeeRegistrationEvent(
            attendee.getEmail(),
            attendee.getFullName(),
            attendee.getRegistrationDate()
        );

        attendeeRegistrationEvent.fire(event);
        logger.info("Event published successfully");
    }
}