package com.conference.attendees.repository;

import com.conference.attendees.model.AttendeeEntity;
import jakarta.persistence.EntityManager;
import jakarta.persistence.NoResultException;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;
import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;

/**
 * Traditional DAO pattern for attendee persistence.
 * This will be refactored to DDD Repository later.
 */
@ApplicationScoped
public class AttendeeRepository {

    private static final Logger logger = Logger.getLogger(AttendeeRepository.class.getName());

    @PersistenceContext(unitName = "attendeePU")
    private EntityManager entityManager;

    @Transactional
    public AttendeeEntity save(AttendeeEntity attendee) {
        logger.info("Saving attendee: " + attendee.getEmail());

        if (attendee.getId() == null) {
            entityManager.persist(attendee);
            logger.info("Persisted new attendee with ID: " + attendee.getId());
            return attendee;
        } else {
            AttendeeEntity merged = entityManager.merge(attendee);
            logger.info("Updated attendee with ID: " + merged.getId());
            return merged;
        }
    }

    public Optional<AttendeeEntity> findById(Long id) {
        logger.info("Finding attendee by ID: " + id);
        AttendeeEntity attendee = entityManager.find(AttendeeEntity.class, id);
        return Optional.ofNullable(attendee);
    }

    public Optional<AttendeeEntity> findByEmail(String email) {
        logger.info("Finding attendee by email: " + email);

        try {
            TypedQuery<AttendeeEntity> query = entityManager.createNamedQuery(
                "AttendeeEntity.findByEmail", AttendeeEntity.class);
            query.setParameter("email", email);
            AttendeeEntity attendee = query.getSingleResult();
            return Optional.of(attendee);
        } catch (NoResultException e) {
            logger.info("No attendee found with email: " + email);
            return Optional.empty();
        }
    }

    public List<AttendeeEntity> findAll() {
        logger.info("Finding all attendees");

        TypedQuery<AttendeeEntity> query = entityManager.createNamedQuery(
            "AttendeeEntity.findAll", AttendeeEntity.class);
        return query.getResultList();
    }

    public List<AttendeeEntity> findAll(int offset, int limit) {
        logger.info("Finding attendees with pagination - offset: " + offset + ", limit: " + limit);

        TypedQuery<AttendeeEntity> query = entityManager.createNamedQuery(
            "AttendeeEntity.findAll", AttendeeEntity.class);
        query.setFirstResult(offset);
        query.setMaxResults(limit);
        return query.getResultList();
    }

    public long count() {
        logger.info("Counting all attendees");

        TypedQuery<Long> query = entityManager.createQuery(
            "SELECT COUNT(a) FROM AttendeeEntity a", Long.class);
        return query.getSingleResult();
    }

    @Transactional
    public void delete(AttendeeEntity attendee) {
        logger.info("Deleting attendee: " + attendee.getEmail());

        if (!entityManager.contains(attendee)) {
            attendee = entityManager.merge(attendee);
        }
        entityManager.remove(attendee);
    }

    @Transactional
    public void deleteById(Long id) {
        logger.info("Deleting attendee by ID: " + id);

        Optional<AttendeeEntity> attendee = findById(id);
        if (attendee.isPresent()) {
            delete(attendee.get());
        } else {
            logger.warning("Attendee with ID " + id + " not found for deletion");
        }
    }

    public boolean existsByEmail(String email) {
        logger.info("Checking if attendee exists with email: " + email);

        TypedQuery<Long> query = entityManager.createQuery(
            "SELECT COUNT(a) FROM AttendeeEntity a WHERE a.email = :email", Long.class);
        query.setParameter("email", email);
        return query.getSingleResult() > 0;
    }
}